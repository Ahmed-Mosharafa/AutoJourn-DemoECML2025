import React, { useState, useEffect } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import { Chart as ChartJS, ArcElement, Tooltip, Legend} from "chart.js";
import { Pie } from "react-chartjs-2";
import ChartDataLabels from "chartjs-plugin-datalabels";
import ReactMarkdown from "react-markdown";
import "./TopicsPage.css";

// Register required Chart.js components
ChartJS.register(ArcElement, Tooltip, Legend, ChartDataLabels);

const TopicsPage = () => {
  const location = useLocation();
  const navigate = useNavigate();

  const { topics, originalText } = location.state || {};

  const [summaries, setSummaries] = useState<{ [key: string]: string }>({});
  const [selectedSummary, setSelectedSummary] = useState<string | null>(null);
  const [hoveredTopic, setHoveredTopic] = useState<string | null>(null); // Track the hovered topic
  const [loadingSummary, setLoadingSummary] = useState<boolean>(false); // Loading state for summary

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

  // Handle bubble click
  const handleBubbleClick = async (topicName: string) => {
    setLoadingSummary(true); // Set loading state
    try {
      const response = await fetch("http://127.0.0.1:8787/topics/Mistral/summaries");
      if (response.ok) {
        const data = await response.json();
        const updatedSummaries = data.summaries.reduce(
          (acc: { [key: string]: string }, item: { topic: string; summary: string }) => {
            acc[item.topic] = item.summary;
            return acc;
          },
          {}
        );

        setSummaries(updatedSummaries); // Update all summaries
        setSelectedSummary(updatedSummaries[topicName] || "Summary not available."); // Update selected summary
      } else {
        console.error("Failed to re-fetch summaries.");
        setSelectedSummary("Click on the Topic to see Summary");
      }
    } catch (error) {
      console.error("Error re-fetching summaries:", error);
      setSelectedSummary("An error occurred while fetching the summary.");
    } finally {
      setLoadingSummary(false); // Reset loading state
    }
  };

  // Prepare data for pie chart
  const chartData = {
    labels: Object.keys(topics),
    datasets: [
      {
        data: Object.values(topics),
        backgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF"], // Assign colors to topics
        hoverBackgroundColor: ["#FF6384", "#36A2EB", "#FFCE56", "#4BC0C0", "#9966FF"],
      },
    ],
  };
  

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

        {/* New Topics List */}
        <div className="topics-list-container">
          
          <div className="division">
              <div className="subcolumn">
                 {/* Bubble visualization for topics */}
                 <h2>Suggested Topics</h2>
                 <p>Click on Each Topic to generate a Summary</p>
                 
                  <div className="topics-bubbles">
                    {Object.entries(topics).map(([topicName, percentage], index) => (
                      <div
                        key={index}
                        className="bubble"
                        style={{
                          width: 100,
                          height: 90,
                        }}
                        data-percentage={`${percentage}%`}
                        onClick={() => handleBubbleClick(topicName)} // Re-fetch summaries on click
                        onMouseEnter={() => setHoveredTopic(`${topicName} (${percentage}%)`)} // Set tooltip text on hover
                        onMouseLeave={() => setHoveredTopic(null)} // Clear tooltip text on mouse leave
                      >
                        <span className="bubble-text">{topicName}</span>
                      </div>
                    ))}
                    {hoveredTopic && <div className="tooltip">{hoveredTopic}</div>}
                  </div>
              </div>
              <div className="subcolumn">
                {/* Pie Chart */}
                <div className="chart-container">
                  <h2>Topic Distribution</h2>
                  <Pie data={chartData}/>
                </div>
              </div>
          </div>
          
        </div>

        <button className="back-button" onClick={() => navigate("/")}>
          Back to Home
        </button>
      </div>

      {/* Second Column */}
      <div className="topics-right">
        <h1>Summary</h1>
        <div className="summary-container">
         <div className="scrollable-text-summary">
          {loadingSummary ? (
            <p>Loading summary...</p>
          ) : selectedSummary ? (
            <ReactMarkdown>{selectedSummary}</ReactMarkdown>
          ) : (
            <div className="summary-placeholder">
              <p>Select a topic to view the summary here.</p>
            </div>
          )}
          </div>
        </div>

        


      </div>
    </div>
  );
};

export default TopicsPage;
