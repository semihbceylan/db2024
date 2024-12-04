import { EvmChain } from '@moralisweb3/common-evm-utils';
import Moralis from 'moralis';

import { ethers } from 'ethers';
import 'dotenv/config';
import fs from "fs";

function dump (_data, _table) {
    let content = _data.map(row => row.join(",")).join("\n");
    fs.writeFile(`./out/${_table}.csv`, content, (err) => {
        if (err) {throw err;} console.log(`${_table}.csv created.`);
    });
}

await Moralis.start({ apiKey: process.env.MORALIS_API_KEY }); 

const chains = [["chain_id", "chain_name",  "native_currency", "explorer_url", "rpc_url"]];
const blocks = [["block_number", "chain_id", "block_hash", "parent_hash", "miner", "transaction_count", "timestamp"]];
const transactions = [["tx_hash", "from_address", "to_address", "block_number", "chain_id", "timestamp", "value"]];
const addresses = [["address", "is_contract", "eth_balance", "erc20_count", "dollar_balance", "nft_count"]];
const nfts = [["address", "chain_id", "owner", "token_id", "token_uri", "contract_type"]]; 
const addressSet = new Set();

(async () => {
    const chainIDs = [1, 10, 100, 137, 8453/*, 42161, 43114, 59144*/]; const providers = []; for (const chainID of chainIDs) {
        const _chain = EvmChain.create(chainID); const _providers = _chain._chainlistData.rpc.filter(url => !url.includes('${')).map(url => new ethers.providers.JsonRpcProvider(url)); for (const _provider of _providers) {
            try {
                const chainId = await _provider.getNetwork().then(network => network.chainId); providers.push(_provider); 
                chains.push([chainID, _chain._chainlistData.name, _chain._chainlistData.nativeCurrency.symbol, _chain._chainlistData.explorers[0].url, _provider.connection.url]);
                break;
            } catch (error) {console.error("Not working RPC URL: ", _provider.connection.url);}
        }
    } // console.log(chains);

    for (let i = 0; i < chainIDs.length; i++) { const _chainID = chainIDs[i]; const _provider = providers[i];
        const latestBlockNumber = await _provider.getBlockNumber(); for (let _blockNumber = 2068621; _blockNumber < 2068622 && _blockNumber <= latestBlockNumber; _blockNumber++) {
            let { hash, parentHash, miner, timestamp, transactions: _transactions } = await _provider.getBlockWithTransactions(_blockNumber);
            timestamp = new Date(timestamp * 1000); timestamp = timestamp.toISOString().replace("T", " ").split(".")[0];
            blocks.push([_blockNumber, _chainID, hash, parentHash, miner, _transactions.length, timestamp]);
            
            for (let _transaction of _transactions) {
                let { hash: txHash, from: fromAddress, to: toAddress, value } = _transaction; value = Number(value._hex) / 1e18;
                transactions.push([txHash, fromAddress, toAddress, _blockNumber, _chainID, timestamp, value]);
                addressSet.add(fromAddress); addressSet.add(toAddress);
            }
        }
    } // console.log(blocks); console.log(transactions); console.log(addressSet);

    for (let _address of addressSet) {
        let isContract = false; let ethBalance = 0; let erc20Count = 0; let dollarBalance = 0; let nftCount = 0;
        for (let i = 0; i < chainIDs.length; i++) { const _chainID = chainIDs[i]; const _provider = providers[i];
            const _chain = EvmChain.create(_chainID);

            // isContract = (isContract) ? true : (await _provider.getCode(_address)) !== "0x";
            
            const _erc20s = (await Moralis.EvmApi.wallets.getWalletTokenBalancesPrice({address: _address, chain: _chain})).result;
            const _nfts = (await Moralis.EvmApi.nft.getWalletNFTs({address: _address, chain: _chain})).result;
            
            ethBalance += (await Moralis.EvmApi.balance.getNativeBalance({address: _address, chain: _chain})).toJSON().balance / (10**18);
            dollarBalance += _erc20s.reduce((acc, token) => acc + token.usdValue, 0);
            erc20Count += _erc20s.length;
            nftCount = _nfts.length;
            
            if (nftCount > 0) {
                for (const _nft of _nfts) {
                    let _tokenUri = null;
                    if (_nft.tokenUri?.slice(0, 34) == "https://ipfs.moralis.io:2053/ipfs/") {
                        _tokenUri = _nft.tokenUri.slice(34, 80);
                        nfts.push([_nft.tokenAddress._value, _chainID, _address, _nft.tokenId, _tokenUri, _nft.contractType]);
                    }
                }
            }
        }

        addresses.push([_address, isContract, ethBalance, erc20Count, dollarBalance, nftCount]);
    } // console.log(addresses); console.log(nfts);

    dump(chains, "chains");
    dump(blocks, "blocks");
    dump(transactions, "transactions");
    dump(addresses, "addresses");
    dump(nfts, "nfts");
})();

