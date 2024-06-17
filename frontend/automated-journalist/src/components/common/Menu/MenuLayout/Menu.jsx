import "./Menu.css";
import { MenuItem } from "../MenuItem/MenuItem";
import homeIcon from "../../../../assets/icons/home.png";
import searchIcon from "../../../../assets/icons/search.png";
import settingsIcon from "../../../../assets/icons/settings.png";
import { useNavigate } from "react-router-dom";

export function Menu() {
  const navigate = useNavigate();

  return (
    <div className="menu-div">
      <MenuItem icon={homeIcon} text="Home" onClick={() => navigate("/feed")} />
      <MenuItem icon={searchIcon} text="Search" />
      <MenuItem
        icon={settingsIcon}
        text="Settings"
        onClick={() => navigate("/settings")}
      />
    </div>
  );
}
