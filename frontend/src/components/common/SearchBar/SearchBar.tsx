import "./SearchBar.css";
import searchIcon from "../../../assets/icons/search.png";
import { Input } from "@mui/material";
import { useState } from "react";

export function SearchBar({ setSearchQuery }: { setSearchQuery: (query: string) => void }) {
  const [query, setQuery] = useState("");

  const handleSearch = () => {
    setSearchQuery(query);
  };

  return (
    <div className="search-bar-container">
      <img
        loading="lazy"
        src={searchIcon}
        className="search-icon"
        onClick={handleSearch}
        alt="Search Icon"
      />
      <Input
        className="search-bar-inner"
        placeholder="Search..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button onClick={handleSearch}>Search</button>
    </div>
  );
}
