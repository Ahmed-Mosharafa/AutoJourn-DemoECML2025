import React, { useState } from "react";
import "./Popup.css";

interface TopicInputPopupProps {
  onClose: () => void;
  onSave: (topics: string[]) => void;
}

const TopicInputPopup: React.FC<TopicInputPopupProps> = ({ onClose, onSave }) => {
  const [topics, setTopics] = useState<string[]>([""]);

  const handleTopicChange = (index: number, event: React.ChangeEvent<HTMLInputElement>) => {
    const newTopics = [...topics];
    newTopics[index] = event.target.value;
    setTopics(newTopics);
  };

  const handleAddTopic = () => {
    setTopics([...topics, ""]);
  };

  const handleRemoveTopic = (index: number) => {
    const newTopics = topics.filter((_, i) => i !== index);
    setTopics(newTopics);
  };

  const handleSave = () => {
    onSave(topics.filter(topic => topic.trim() !== "")); // Save non-empty topics
    onClose(); // Close the popup
  };

  return (
    <div className="popup-overlay">
      <div className="popup-content">
        <h2>Add Topics</h2>
        {topics.map((topic, index) => (
          <div key={index} className="topic-input">
            <input
              type="text"
              value={topic}
              onChange={(event) => handleTopicChange(index, event)}
              placeholder={`Topic ${index + 1}`}
            />
            <button onClick={() => handleRemoveTopic(index)} disabled={topics.length === 1}>
              Remove
            </button>
          </div>
        ))}
        <button onClick={handleAddTopic}>Add Another Topic</button>
        <div className="popup-actions">
          <button onClick={handleSave}>Save</button>
          <button onClick={onClose}>Cancel</button>
        </div>
      </div>
    </div>
  );
};

export default TopicInputPopup;
