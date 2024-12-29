import "../styles/sections.css"



function LeftSection() {
  return (
    <div className="left-section">
      <div className="text-content">
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. In malesuada
        euismod aliquam. Suspendisse et purus at felis tincidunt rhoncus. Proin
        sagittis quis ipsum eu laoreet. Quisque in laoreet arcu. Suspendisse
        eget placerat magna. Quisque in vehicula ante. Donec condimentum est sit
        amet lectus luctus tempus. Pellentesque habitant morbi tristique
        senectus et netus et malesuada fames ac turpis egestas. Nullam vel
        luctus eros, ut ultricies magna. Lorem ipsum dolor sit amet, consectetur
        adipiscing elit. Nulla facilisis ipsum justo, eu sagittis sapien aliquet
        gravida. Aliquam blandit justo ligula, eu viverra enim venenatis eu.
        Pellentesque egestas fringilla enim sit amet lacinia.
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
      <RightSection />
    </div>
  )
}