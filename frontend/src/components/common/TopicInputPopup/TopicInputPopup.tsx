import React, { useState } from "react";
import "./Popup.css";

interface TopicInputPopupProps {
  onClose: () => void;
  onSave: (selectedOption: string) => void;
}

const TopicInputPopup: React.FC<TopicInputPopupProps> = ({ onClose, onSave }) => {
  const [selectedOption, setSelectedOption] = useState<string>("");

  const handleOptionChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSelectedOption(event.target.value);
  };

  const handleSave = () => {
    if (selectedOption.trim() !== "") {
      onSave(selectedOption); // Save the selected option
      onClose(); // Close the popup
    } else {
      alert("Please select an option before saving.");
    }
  };

  return (
    <div className="popup-overlay">
      <div className="popup-content">
        <h2>Select Topic Modelling Method</h2>
        <div>
          <label>
            <input
              type="radio"
              name="topicModelling"
              value="Mistral"
              checked={selectedOption === "Mistral"}
              onChange={handleOptionChange}
            />
            Topic Modelling with Mistral
          </label>
        </div>
        <div>
          <label>
            <input
              type="radio"
              name="topicModelling"
              value="Phi"
              checked={selectedOption === "Phi"}
              onChange={handleOptionChange}
            />
            Topic Modelling with Phi
          </label>
        </div>
        <div className="popup-actions">
          <button onClick={handleSave}>Save</button>
          <button onClick={onClose}>Cancel</button>
        </div>
      </div>
    </div>
  );
};

export default TopicInputPopup;
