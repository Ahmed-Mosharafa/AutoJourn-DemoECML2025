import "./SearchBar.css";
import searchIcon from "../../../assets/icons/search.png";
import { Input } from "@mui/material";
import { useState } from "react";

export function SearchBar({ setSearchQuery }: { setSearchQuery: (query: string) => void }) {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false); // Loading state

  const handleSearch = async () => {
    setLoading(true); // Show loading screen
    try {
      await new Promise((resolve) => setTimeout(resolve, 2000)); // Simulate loading delay
      setSearchQuery(query);
    } catch (error) {
      console.error("Error during search:", error);
    } finally {
      setLoading(false); // Hide loading screen
    }
  };

  return (
    <div className="search-bar-wrapper">
      {loading && (
        <div className="loading-overlay">
          <div className="spinner"></div>
          <p>Loading results...</p>
        </div>
      )}
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
    </div>
  );
}
