import { useState } from "react";
import { ApiSelector } from "../common/ApiSelector/ApiSelectorLayout/ApiSelector";
import "./Feed.css";

export function Feed() {
  const [selectedAPI, setSelectedAPI] = useState("");

  return (
    <div className="api-selector">
      <ApiSelector setSelectedAPI={setSelectedAPI} />
    </div>
  );
}
