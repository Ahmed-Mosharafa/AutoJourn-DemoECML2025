import { FormControl, InputLabel, MenuItem, Select, SelectChangeEvent } from "@mui/material";
import { Samsum } from "../../backend-objects/Samsum";
import "./Summary.css";
import { useState } from "react";

interface SummaryProps {
  selectedDialogue: Samsum | null;
}

export function Summary({selectedDialogue}: SummaryProps) {
  const [selectedSummaryTopic, setSelectedSummaryTopic] = useState('');
  const summaryTopicList = ["Topic 1","Topic 2","Topic 3"]
  const handleChange = (event: SelectChangeEvent) => {
    setSelectedSummaryTopic(event.target.value as string);
  };
  const topicTitle = "Topic: ";
  const topic = "US Elections";
  const summaryTime = "Summarized: 3 min ago";
  const summaryTitle = "Summary";
  const topicSelectTitle = "Topic";
  
  return <>
  <div className="summary-page">
    <div className="topic-area">
      <div className="topic-title">{topicTitle}</div>
      <div className="topic">{topic}</div>
    </div>
    <div className="summarize-time">{summaryTime}</div>
    <div className="dropdown-area">
      <FormControl sx={{m:1, width: 180 }}>
        <InputLabel id="demo-simple-select-label">{topicSelectTitle}</InputLabel>
        <Select
          labelId="demo-simple-select-label"
          id="demo-simple-select"
          value={selectedSummaryTopic}
          label="Topic"
          onChange={handleChange}
        >
          {summaryTopicList.map((summaryTopic)=>(
            <MenuItem value={summaryTopic}>{summaryTopic}</MenuItem>
          ))}
        </Select>
      </FormControl>
    </div>
    <div className="summary-title">{summaryTitle}</div>
    <div className="summary">
      {selectedDialogue?.summary}
    </div>
    <div className="divider" />
  </div>
  </>;
}
