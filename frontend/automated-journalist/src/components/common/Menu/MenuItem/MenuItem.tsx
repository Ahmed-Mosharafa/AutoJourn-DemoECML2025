import { MouseEventHandler } from "react";
import "./MenuItem.css";

interface MenuItemProps {
  text: string;
  icon: string;
  onClick: MouseEventHandler;
}

export function MenuItem({ text, icon, onClick }: MenuItemProps) {
  return (
    <div className="item-container" onClick={onClick}>
      <img loading="lazy" src={icon} className="item-icon" />
      <div className="item-text">{text}</div>
    </div>
  );
}
