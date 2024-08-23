export default function CountDiv(props) {
  return (
    <>
      <div className="customer-container">
        <div className="customer-grid">
          <div className="customer-count-info">
            <div>
              <label className="customer-count-head">{props.title}</label>
            </div>
            <div>
              <label className="number">{props.customercount}</label>
            </div>
          </div>
          <div>
            <img src={props.image} alt="image" />
          </div>
        </div>
      </div>
    </>
  );
}
