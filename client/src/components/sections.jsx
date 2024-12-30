import "../styles/sections.css"



function LeftSection() {
  return (
    <div className="left-section">
      <div className="text-content">
	  Databees is a multichain block explorer that operates on SQL. Unlike standard block explorers, it keeps a portion of data cached, significantly enhancing search performance. If the search parameters fall within the cached data, Databees can deliver results without querying the blockchain directly, enabling faster responses to users.
      </div>
      <div className="icons-container">
        <IconCircle color="#1a2b3c">M</IconCircle>
        <IconCircle color="#ff0000">OP</IconCircle>
        <IconCircle color="#0000ff">−</IconCircle>
        <IconCircle color="#800080">∞</IconCircle>
        <IconCircle color="#6495ed">Ξ</IconCircle>
        <IconCircle color="#90ee90">V</IconCircle>
      </div>
    </div>
  )
}

function RightSection() {
  return (
    <div className="right-section">
      <div className="form-container">
        <input type="text" className="input-field" placeholder="Text Input" />
        <div className="select-container">
          <button className="select-button">Select</button>
          <button className="select-button">Select</button>
        </div>
        <button className="action-button">Button - Explore the Blocks</button>
        <button className="action-button">Button - or Explore the NFTs</button>
      </div>
    </div>
  )
}

function IconCircle({ color, children }) {
  return (
    <div
      className="icon"
      style={{
        backgroundColor: color,
        color: color === "#ff0000" ? "white" : "white"
      }}
    >
      {children}
    </div>
  )
}

export default function Sections() {
  return (
    <div className="sections">
      <LeftSection />
      {/*<RightSection />*/}
    </div>
  )
}