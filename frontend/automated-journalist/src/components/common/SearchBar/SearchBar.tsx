import "./SearchBar.css";
import searchIcon from "../../../assets/icons/search.png";
import { Input } from "@mui/material";
import { useState } from "react";


export function SearchBar({ setSearchQuery}: { setSearchQuery: (query: string) => void }){
  const [query, setQuery] = useState(""); 

  return (
    <>
      <div className="search-bar-container">
        <img loading="lazy" src={searchIcon} className="search-icon" />
        <Input slotProps={{ input: { className: 'search-bar-inner' } }} onChange={(e) => setQuery(e.target.value) } />
        <button onClick={() => {setSearchQuery(query)}}> Search</button>
      </div>
    </>
  );
}
