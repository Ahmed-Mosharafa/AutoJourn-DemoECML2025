import "./MenuItem.css";

interface MenuItemProps {
  text: string;
  icon: string;
}

export function MenuItem({ text, icon }: MenuItemProps) {
  return (
    <div className="item-container">
      <img loading="lazy" src={icon} className="item-icon" />
      <div className="item-text">{text}</div>
    </div>
  );
}
