import {Dialog, DialogTitle, FormControl, InputLabel, MenuItem, Select, SelectChangeEvent} from "@mui/material";
import {useState} from "react";
import {useNavigate} from "react-router-dom";


interface SummaryProps {
    dialogOpen:boolean;
    closeDialog: ()=>void;
    selectedCompareTopic1:string;
    selectedCompareTopic2:string;
    summaryTopicList:string[];
    setSelectedCompareTopic1: React.Dispatch<React.SetStateAction<string>>
    setSelectedCompareTopic2: React.Dispatch<React.SetStateAction<string>>
}

export function CompareSummariesDialog({dialogOpen, closeDialog, selectedCompareTopic1,selectedCompareTopic2,summaryTopicList,setSelectedCompareTopic1,setSelectedCompareTopic2}:SummaryProps)
{
    const navigate = useNavigate();
    const topicSelectTitle = "Topic";

    const selectCompareTopic1 = (event: SelectChangeEvent) => {
        setSelectedCompareTopic1(event.target.value as string);
    }
    const selectCompareTopic2 = (event: SelectChangeEvent) => {
        setSelectedCompareTopic2(event.target.value as string);
    }

    const compareSummaries = () => {
        navigate('/compare-summaries');
    }

    const getSummaryTopicList = (selectedCompareTopic:string | undefined):string[] | undefined => {
        if(selectedCompareTopic==selectedCompareTopic1){
            return summaryTopicList.filter(topic => topic !== selectedCompareTopic2);
        }
        if(selectedCompareTopic==selectedCompareTopic2){
            return summaryTopicList.filter(topic => topic !== selectedCompareTopic1);
        }
    };

    return <>
        <Dialog open={dialogOpen} onClose={closeDialog}>
            <div className="compare-dialog">
                <DialogTitle>Compare Summaries</DialogTitle>
                <h3>Topic 1:</h3>
                <FormControl sx={{m: 1, width: 180}}>
                    <InputLabel id="demo-simple-select-label">{topicSelectTitle}</InputLabel>
                    <Select
                        labelId="demo-simple-select-label"
                        id="demo-simple-select"
                        value={selectedCompareTopic1}
                        label="Topic"
                        onChange={selectCompareTopic1}
                    >
                        {getSummaryTopicList(selectedCompareTopic1)?.map((summaryTopic) => (
                            <MenuItem value={summaryTopic}>{summaryTopic}</MenuItem>
                        ))}
                    </Select>
                </FormControl>
                <h3>Topic 2:</h3>
                <FormControl sx={{m: 1, width: 180}}>
                    <InputLabel id="demo-simple-select-label">{topicSelectTitle}</InputLabel>
                    <Select
                        labelId="demo-simple-select-label"
                        id="demo-simple-select"
                        value={selectedCompareTopic2}
                        label="Topic"
                        onChange={selectCompareTopic2}
                    >
                        {getSummaryTopicList(selectedCompareTopic2)?.map((summaryTopic) => (
                            <MenuItem value={summaryTopic}>{summaryTopic}</MenuItem>
                        ))}
                    </Select>
                </FormControl>
                <div>
                    <button className="compare-button" disabled={selectedCompareTopic1=='' || selectedCompareTopic2==''} onClick={compareSummaries}>Compare</button>
                </div>
            </div>
        </Dialog>
    </>
}
