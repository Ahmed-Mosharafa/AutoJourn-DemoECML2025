import "./ApiSelectorItem.css";

interface ApiSelectorItemProps {
  text: string;
}

export function ApiSelectorItem({ text }: ApiSelectorItemProps) {
  return (
    <>
      <div className="api-selector-text">{text}</div>
    </>
  );
}
