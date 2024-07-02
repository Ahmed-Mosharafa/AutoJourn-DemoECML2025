import scatterPlot from '../../assets/scatter_plot.png';
import cosineSimilarityMatrix from '../../assets/cosine_similarity_matrix.png';
import {FormControlLabel, Switch} from "@mui/material";
import "./CompareSummaries.css"
import {useState} from "react";
import {useFetchDeltaSummarize} from "../../hooks/APIHooks";

interface CompareSummariesProps {
    selectedCompareTopic1:string;
    selectedCompareTopic2:string;
}

// const requestData = {
//     summaries: {
//         "0_you_it_the_to": "Benjamin, Hilary, Elliot and Daniel are going to meet for drinks in the evening. They will go back to the apartment together. Benjamin will come at lunchtime and take the keys.",
//         "5_the_we_world_and": "Benjamin is having lunch with some French people who work on the history of food in colonial Mexico. He's yawning and wants to take a nap.",
//         "8_due_august_tuesday_july": "Hilary is meeting them at the entrance to the"
//     },
//     plot_type: '2d_scatter_plot', // cosine_similarity
// };

export function CompareSummaries({selectedCompareTopic1, selectedCompareTopic2} : CompareSummariesProps){
    const graphTypes = ["Scatter Plot", "Cosine Similarity Matrix"];
    const [switchLabel, setSwitchLabel] = useState(graphTypes[0]);
    const [checked, setChecked] = useState(false);
    const [requestData, setRequestData] = useState({
        summaries: {
            "0_you_it_the_to": "Benjamin, Hilary, Elliot and Daniel are going to meet for drinks in the evening. They will go back to the apartment together. Benjamin will come at lunchtime and take the keys.",
            "5_the_we_world_and": "Benjamin is having lunch with some French people who work on the history of food in colonial Mexico. He's yawning and wants to take a nap.",
            "8_due_august_tuesday_july": "Hilary is meeting them at the entrance to the"
        },
        plot_type: '2d_scatter_plot', // cosine_similarity
    });

    const { imageSrc, loading, error } = useFetchDeltaSummarize(requestData);

    const handleChange = (event : React.ChangeEvent<HTMLInputElement>) => {
        setChecked(event.target.checked);
        if(checked){
            setSwitchLabel(graphTypes[0])
            setRequestData({
                summaries: {
                    "0_you_it_the_to": "Benjamin, Hilary, Elliot and Daniel are going to meet for drinks in the evening. They will go back to the apartment together. Benjamin will come at lunchtime and take the keys.",
                    "5_the_we_world_and": "Benjamin is having lunch with some French people who work on the history of food in colonial Mexico. He's yawning and wants to take a nap.",
                    "8_due_august_tuesday_july": "Hilary is meeting them at the entrance to the"
                },
                plot_type: '2d_scatter_plot', // cosine_similarity
            })
        }
        else {
            setSwitchLabel(graphTypes[1])
            setRequestData({
                summaries: {
                    "0_you_it_the_to": "Benjamin, Hilary, Elliot and Daniel are going to meet for drinks in the evening. They will go back to the apartment together. Benjamin will come at lunchtime and take the keys.",
                    "5_the_we_world_and": "Benjamin is having lunch with some French people who work on the history of food in colonial Mexico. He's yawning and wants to take a nap.",
                    "8_due_august_tuesday_july": "Hilary is meeting them at the entrance to the"
                },
                plot_type: 'cosine_similarity', // cosine_similarity
            })
        }
    };




    return <>
        <div className="compare-summary-page">
            <div className="title-area">
                Compare Summaries: {selectedCompareTopic1} and {selectedCompareTopic2}
            </div>
            <FormControlLabel
                control={
                    <Switch checked={checked} onChange={handleChange} defaultChecked color="default"/>
                }
                label={switchLabel}
            />
            <div>
                {imageSrc && <img src={imageSrc} style={{maxWidth: '600px', height: 'auto'}} />}
            </div>
        </div>
    </>
}