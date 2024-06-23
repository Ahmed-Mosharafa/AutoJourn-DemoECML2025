import "./SearchBar.css";
import searchIcon from "../../../assets/icons/search.png";
import { Input } from "@mui/material";


export function SearchBar() {
  return (
    <>
      <div className="search-bar-container">
        <img loading="lazy" src={searchIcon} className="search-icon" />
        <Input slotProps={{ input: { className: 'search-bar-inner' } }} />
      </div>
    </>
  );
}
