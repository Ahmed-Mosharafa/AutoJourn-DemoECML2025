import "./Menu.css";
import { MenuItem } from "../MenuItem/MenuItem";
import homeIcon from "../../../../assets/icons/home.png";
import searchIcon from "../../../../assets/icons/search.png";
import settingsIcon from "../../../../assets/icons/settings.png";

export function Menu() {
  return (
    <div className="menu-div">
      <MenuItem icon={homeIcon} text="Home" />
      <MenuItem icon={searchIcon} text="Search" />
      <MenuItem icon={settingsIcon} text="Settings" />
    </div>
  );
}
