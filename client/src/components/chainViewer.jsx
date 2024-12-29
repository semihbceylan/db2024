import { LatestBlocks } from "./latestBlocks"
import { LatestTransactions } from "./latestTransactions"
import "../styles/chainViewer.css"

export function ChainViewer() {
  return (
    <div className="chain-viewer-container">
      <LatestBlocks />
      <LatestTransactions />
    </div>
  )
}
