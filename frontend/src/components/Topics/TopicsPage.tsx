import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import "./TopicsPage.css";

const TopicsPage = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const { topics, originalText } = location.state || {};

  const [summaries, setSummaries] = useState<{ [key: string]: string }>({});
  const [selectedSummary, setSelectedSummary] = useState<string | null>(null);

  // Fetch summaries when the component mounts
  useEffect(() => {
    const fetchSummaries = async () => {
      try {
        const response = await fetch("http://127.0.0.1:8787/topics/Mistral/summaries");
        if (response.ok) {
          const data = await response.json();
          setSummaries(
            data.summaries.reduce(
              (acc: { [key: string]: string }, item: { topic: string; summary: string }) => {
                acc[item.topic] = item.summary;
                return acc;
              },
              {}
            )
          );
        } else {
          console.error("Failed to fetch summaries.");
        }
      } catch (error) {
        console.error("Error fetching summaries:", error);
      }
    };

    fetchSummaries();
  }, []);

  if (!topics || !originalText) {
    return (
      <div className="topics-page">
        <h2>No topics to display</h2>
        <button onClick={() => navigate("/")}>Go Back</button>
      </div>
    );
  }

  return (
    <div className="topics-container">
      {/* First Column */}
      <div className="topics-left">
        <h1>Extracted Topics</h1>

        {/* Scrollable division for the original text */}
        <div className="original-text-container">
          <h2>Original Text:</h2>
          <div className="scrollable-text">
            <p>{originalText}</p>
          </div>
        </div>

        {/* Bubble visualization for topics */}
        <div className="topics-bubbles">
          {Object.entries(topics).map(([topicName, percentage], index) => (
            <div
              key={index}
              className="bubble"
              style={{
                width: `${percentage}%`,
                height: `${percentage}%`,
              }}
              data-percentage={`${percentage}%`} // Pass percentage for hover display
              onClick={() => setSelectedSummary(summaries[topicName] || "Summary not available.")}
            >
              <span className="bubble-text">{topicName}</span>
            </div>
          ))}
        </div>

        <button className="back-button" onClick={() => navigate("/")}>
          Back to Home
        </button>
      </div>

      {/* Second Column */}
      <div className="topics-right">
        <h1>Summary</h1>
        <div className="summary-container">
          {selectedSummary ? (
            <p>{selectedSummary}</p>
          ) : (
            <div className="summary-placeholder">
              <p>Select a topic to view the summary here.</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default TopicsPage;
