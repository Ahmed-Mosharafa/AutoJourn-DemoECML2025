import { FormControl, InputLabel, MenuItem, Select, SelectChangeEvent } from "@mui/material";
import { Samsum } from "../../backend-objects/Samsum";
import "./Summary.css";
import { useEffect, useState } from "react";
import { useSummarize, useTopicAwareSummarize } from "../../hooks/APIHooks";
import CircularLoader from "../common/Loader/CircularLoader";
import useStore from "../../store/store";

interface SummaryProps {
  selectedDialogue: Samsum | null;
}

export function Summary({ selectedDialogue }: SummaryProps) {
  const { fetchSummary, summary, loading, error } = useSummarize([selectedDialogue ?? { id: "-1", summary: "", dialogue: "" }])
  const { fetchTopicAwareSummary, summaries: topicAwareSummaries, loading: topicAwareLoading, error: topicAwareError } = useTopicAwareSummarize(selectedDialogue ?? { id: "-1", summary: "", dialogue: "" })
  const { searchQuery, isSummarize } = useStore();
  const [selectedSummaryTopic, setSelectedSummaryTopic] = useState("Default");
  const summaryTopicList = Object.keys(topicAwareSummaries ?? {});
  summaryTopicList.unshift("Default");
  const handleChange = (event: SelectChangeEvent) => {
    setSelectedSummaryTopic(event.target.value as string);
  };
  const topicTitle = "Topic: ";
  const topic = searchQuery;
  const summaryTime = "Summarized: 3 min ago";
  const summaryTitle = "Summary";
  const topicSelectTitle = "Topic";

  useEffect(() => {
    if (isSummarize) {
      fetchSummary();
      fetchTopicAwareSummary();
    }
  }, [isSummarize])

  if (loading || topicAwareLoading) {
    return <CircularLoader />
  }
  if (error || topicAwareError) {
    return <div> {error}</div>
  }
  return <>
    <div className="summary-page">
      <div className="topic-area">
        <div className="topic-title">{topicTitle}</div>
        <div className="topic">{topic}</div>
      </div>
      <div className="summarize-time">{summaryTime}</div>
      <div className="dropdown-area">
        <FormControl sx={{ m: 1, width: 180 }}>
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
        {selectedSummaryTopic !== "Default" ? (topicAwareSummaries ?? {})[selectedSummaryTopic]
          :
          summary?.[0].summary
        }
      </div>
      <div className="divider" />
    </div>
  </>;
}
