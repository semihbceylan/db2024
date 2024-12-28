import { EclipseIcon as Ethereum } from "lucide-react"
import "../styles/chainViewer.css"

export function LatestTransactions() {
  const transactions = [
    {
      hash: "0x153...",
      from: "0xsdfgsdfgsdfgdsfg",
      to: "0xsdfgsdfgsdfgdsfg",
      timestamp: "2016-08-14 05:30:06"
    },
    {
      hash: "0x153...",
      from: "0xsdfgsdfgsdfgdsfg",
      to: "0xsdfgsdfgsdfgdsfg",
      timestamp: "2016-08-14 05:30:06"
    },
    {
      hash: "0x153...",
      from: "0xsdfgsdfgsdfgdsfg",
      to: "0xsdfgsdfgsdfgdsfg",
      timestamp: "2016-08-14 05:30:06"
    },
    {
      hash: "0x153...",
      from: "0xsdfgsdfgsdfgdsfg",
      to: "0xsdfgsdfgsdfgdsfg",
      timestamp: "2016-08-14 05:30:06"
    }
  ]

  return (
    <div className="section">
      <div className="section-header">Latest Transaction for Each Chain</div>
      <div className="section-content">
        {transactions.map((tx, index) => (
          <div key={index} className="block-row">
            <div className="icon-container">
              <Ethereum size={24} />
            </div>
            <div className="block-details">
              <div className="block-number">{tx.hash}</div>
              <div className="block-info">
                <div>
                  From <span className="block-miner">{tx.from}</span>
                </div>
                <div>
                  To <span className="block-miner">{tx.to}</span>
                </div>
              </div>
            </div>
            <div className="timestamp">{tx.timestamp}</div>
          </div>
        ))}
      </div>
    </div>
  )
}
