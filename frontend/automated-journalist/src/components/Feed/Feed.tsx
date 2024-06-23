import { useState } from "react";
import { ApiSelector } from "../common/ApiSelector/ApiSelectorLayout/ApiSelector";
import "./Feed.css";
import { SearchBar } from "../common/SearchBar/SearchBar";

interface FeedProps {
  isSearch?: boolean;
}

Feed.defaultProps = {
  isSearch: false,
};

export function Feed(props: FeedProps) {
  const [selectedAPI, setSelectedAPI] = useState("");

  return (
    <div className="api-selector">
      <ApiSelector setSelectedAPI={setSelectedAPI} />
      {props.isSearch ? <SearchBar /> : <></>}
    </div>
  );
}
