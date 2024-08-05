import { useState } from "react";
import { ApiSelector } from "../common/ApiSelector/ApiSelectorLayout/ApiSelector";
import "./Feed.css";
import { SearchBar } from "../common/SearchBar/SearchBar";
import { useNavigate } from "react-router-dom";
import { Samsum } from "../../backend-objects/Samsum";
import { useFetchSearch } from "../../hooks/APIHooks";
import CircularLoader from "../common/Loader/CircularLoader";
import useStore from "../../store/store";
import { APIConstants } from "../../constants/APIConstants";

interface FeedProps {
  setSelectedDialogue: React.Dispatch<React.SetStateAction<Samsum | null>>;
  isSearch?: boolean;
}

Feed.defaultProps = {
  isSearch: false,
};

export function Feed({ setSelectedDialogue, isSearch }: FeedProps) {
  const navigate = useNavigate();
  const { searchQuery, setSearchQuery, setIsSummarize, conversations } = useStore();
  const [selectedAPI, setSelectedAPI] = useState(APIConstants.REDDIT);
  const [selectedDialogueIndex, setselectedDialogueIndex] = useState(-1);
  const { data: conversationResponse, loading, error } = useFetchSearch(selectedAPI);
  
  const title = "Topic: ";
  let source = `Using ${selectedAPI} API`;
  const buttonText = "Summarize Text";

  const summarizeText = () => {
    if (!conversationResponse) {
      return;
    }
    if (selectedDialogueIndex !== -1) {
      setSelectedDialogue(conversationResponse[selectedDialogueIndex])
      setIsSummarize(true)
      navigate('/summary');
    }
  }

  const selectDialogue = (index: number) => {
    if (selectedDialogueIndex === index) {
      setselectedDialogueIndex(-1);
    } else {
      setselectedDialogueIndex(index);
    }
  }

  if (error) {
    return <div> {error}</div>
  }
  if (loading) {
    return <CircularLoader />
  }
  return (
    <>
      <div className="api-selector">
        <ApiSelector setSelectedAPI={setSelectedAPI} />
        {isSearch ? <SearchBar setSearchQuery={setSearchQuery} /> : <></>}
      </div>
      <div className="dialogues-area">
        <div className="topic-area">
          <div className="topic-title">{title}</div>
          <div className="topic">{searchQuery}</div>
        </div>
        <div className="fetch-time">{source}</div>
        <div className="dialogue-list">
          {(conversations ?? []).map((samsum, index) => (
            <div
              className={`dialogue ${selectedDialogueIndex === index ? 'selected' : ''}`}
              onClick={() => selectDialogue(index)}
              key={samsum.id}> {samsum.dialogue}
            </div>
          ))}
        </div>
        <div className="divider" />
        <div className="divider" />
        <button className="summarize-button" onClick={summarizeText} disabled={selectedDialogueIndex === -1}>{buttonText}</button>
      </div>
    </>
  );
}
