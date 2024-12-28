import { Mail } from "lucide-react"
import "../styles/chainViewer.css"

export function LatestBlocks() {
  const blocks = [
    {
      number: "835625",
      miner: "0xsdfgsdfgsdfgdsfg",
      transactions: 7,
      timestamp: "2016-08-14 05:30:06"
    },
    {
      number: "835625",
      miner: "0xsdfgsdfgsdfgdsfg",
      transactions: 7,
      timestamp: "2016-08-14 05:30:06"
    },
    {
      number: "835625",
      miner: "0xsdfgsdfgsdfgdsfg",
      transactions: 7,
      timestamp: "2016-08-14 05:30:06"
    },
    {
      number: "835625",
      miner: "0xsdfgsdfgsdfgdsfg",
      transactions: 7,
      timestamp: "2016-08-14 05:30:06"
    }
  ]

  return (
    <div className="section">
      <div className="section-header">Latest Blocks for Each Chain</div>
      <div className="section-content">
        {blocks.map((block, index) => (
          <div key={index} className="block-row">
            <div className="icon-container">
              <Mail size={24} />
            </div>
            <div className="block-details">
              <div className="block-number">{block.number}</div>
              <div className="block-info">
                Miner <span className="block-miner">{block.miner}</span>
                <div className="transaction-count">
                  Total Transaction {block.transactions}
                </div>
              </div>
            </div>
            <div className="timestamp">{block.timestamp}</div>
          </div>
        ))}
      </div>
    </div>
  )
}
