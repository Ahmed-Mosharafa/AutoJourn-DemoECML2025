import scatterPlot from '../../assets/scatter_plot.png';
import cosineSimilarityMatrix from '../../assets/cosine_similarity_matrix.png';
import {FormControlLabel, Switch} from "@mui/material";
import "./CompareSummaries.css"
import {useState} from "react";
import {Samsum} from "../../backend-objects/Samsum";

interface CompareSummariesProps {
    selectedCompareTopic1:string;
    selectedCompareTopic2:string;
}

export function CompareSummaries({selectedCompareTopic1, selectedCompareTopic2} : CompareSummariesProps){
    const graphTypes = ["Scatter Plot", "Cosine Similarity Matrix"];
    const [switchLabel, setSwitchLabel] = useState(graphTypes[0]);
    const [checked, setChecked] = useState(false);
    const [imageSource, setImageSource] = useState(scatterPlot);
    const handleChange = (event : React.ChangeEvent<HTMLInputElement>) => {
        setChecked(event.target.checked);
        if(checked){
            setSwitchLabel(graphTypes[0])
            setImageSource(scatterPlot)
        }
        else {
            setSwitchLabel(graphTypes[1])
            setImageSource(cosineSimilarityMatrix)
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
                <img src={imageSource} style={{maxWidth: '600px', height: 'auto'}}/>
            </div>
        </div>
    </>
}