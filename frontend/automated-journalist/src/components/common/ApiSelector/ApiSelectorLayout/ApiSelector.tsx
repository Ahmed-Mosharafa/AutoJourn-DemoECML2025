import { ApiSelectorItem } from "../ApiSelectorItem/ApiSelectorItem";
import "./ApiSelector.css";

export function ApiSelector() {
  return (
    <>
      <div className="api-selector-container">
        <ApiSelectorItem text="Twitter" />
        <ApiSelectorItem text="Reddit" />
        <ApiSelectorItem text="Telegram" />
      </div>
    </>
  );
}
