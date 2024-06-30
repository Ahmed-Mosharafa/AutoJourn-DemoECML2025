import {Dialog, DialogTitle, FormControl, InputLabel, MenuItem, Select, SelectChangeEvent} from "@mui/material";
import { Samsum } from "../../backend-objects/Samsum";
import "./Summary.css";
import { useState } from "react";
import {CompareSummariesDialog} from "../common/CompareSummariesDialog/CompareSummariesDialog";


interface SummaryProps {
  selectedDialogue: Samsum | null;
  selectedCompareTopic1:string;
  selectedCompareTopic2:string;
  setSelectedCompareTopic1: React.Dispatch<React.SetStateAction<string>>
  setSelectedCompareTopic2: React.Dispatch<React.SetStateAction<string>>
}

export function Summary({selectedDialogue, selectedCompareTopic1, selectedCompareTopic2, setSelectedCompareTopic1, setSelectedCompareTopic2}: SummaryProps) {
  const [selectedSummaryTopic, setSelectedSummaryTopic] = useState('');
  const [dialogOpen, setDialogOpen] = useState(false);

  const summaryTopicList:string[] = ["Topic 1","Topic 2","Topic 3"]
  const topicSelectTitle = "Topic";
  const topicTitle = "Topic: ";
  const topic = "US Elections";
  const summaryTime = "Summarized: 3 min ago";
  const summaryTitle = "Summary";
  const buttonText = "Compare Summaries";

  const handleChange = (event: SelectChangeEvent) => {
    setSelectedSummaryTopic(event.target.value as string);
  };

  const openDialog = () => {
    setDialogOpen(true);
  };

  const closeDialog = () => {
    setDialogOpen(false);
  };

  return <>
    <div className="summary-page">
      <div className="topic-area">
        <div className="topic-title">{topicTitle}</div>
        <div className="topic">{topic}</div>
      </div>
      <div className="summarize-time">{summaryTime}</div>
      <div className="dropdown-area">
        <FormControl sx={{m: 1, width: 180}}>
          <InputLabel id="demo-simple-select-label">{topicSelectTitle}</InputLabel>
          <Select
              labelId="demo-simple-select-label"
              id="demo-simple-select"
              value={selectedSummaryTopic}
              label="Topic"
              onChange={handleChange}
          >
            {summaryTopicList.map((summaryTopic) => (
                <MenuItem value={summaryTopic}>{summaryTopic}</MenuItem>
            ))}
          </Select>
        </FormControl>
      </div>
      <div className="summary-title">{summaryTitle}</div>
      <div className="summary">
        {selectedDialogue?.summary}
      </div>
      <div className="divider"/>
      <div className="button-area">
        <button className="compare-summaries-button" onClick={openDialog}>{buttonText}</button>
      </div>
      <CompareSummariesDialog dialogOpen={dialogOpen} closeDialog={closeDialog} selectedCompareTopic1={selectedCompareTopic1} selectedCompareTopic2={selectedCompareTopic2} summaryTopicList={summaryTopicList} setSelectedCompareTopic1={setSelectedCompareTopic1} setSelectedCompareTopic2={setSelectedCompareTopic2}/>
    </div>
  </>;
}
