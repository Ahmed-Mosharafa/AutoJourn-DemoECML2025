import { useState } from "react";
import { ApiSelector } from "../common/ApiSelector/ApiSelectorLayout/ApiSelector";
import "./Feed.css";
import { SearchBar } from "../common/SearchBar/SearchBar";
import { useFetchTelegramSearch } from "../../hooks/APIHooks";

interface FeedProps {
  isSearch?: boolean;
}

Feed.defaultProps = {
  isSearch: false,
};

export function Feed(props: FeedProps) {
  const [selectedAPI, setSelectedAPI] = useState("");
  const [searchQuery, setSearchQuery] = useState("");
  const {data, loading, error} = useFetchTelegramSearch(searchQuery);

  console.log(data, loading, error);

  return (
    <div className="api-selector">
      <ApiSelector setSelectedAPI={setSelectedAPI} />
      {props.isSearch ? <SearchBar setSearchQuery={setSearchQuery}/> : <></>}

      {loading ? (
        <div>Loading...</div>
      ): error ? (
        <div>{error}</div>
      ): (
        data?.map((item) => (
          <div key={item.id}>
            <h3>{item.summary}</h3>
            <p>{item.dialogue}</p>
          </div>
        )
      ) )
      }
    </div>
  );
}
