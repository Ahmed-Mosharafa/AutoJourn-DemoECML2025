import { useState } from "react";
import { ApiSelector } from "../common/ApiSelector/ApiSelectorLayout/ApiSelector";
import "./Feed.css";
import { SearchBar } from "../common/SearchBar/SearchBar";
import { useNavigate } from "react-router-dom";
import { Samsum } from "../../backend-objects/Samsum";

interface FeedProps {
  setSelectedDialogue:React.Dispatch<React.SetStateAction<Samsum | null>>;
  isSearch?: boolean;
}

Feed.defaultProps = {
  isSearch: false,
};

export function Feed({setSelectedDialogue,isSearch}: FeedProps) {
  const navigate = useNavigate();
  const [selectedAPI, setSelectedAPI] = useState("");
  const [selectedDialogueIndex, setselectedDialogueIndex] = useState(-1);
  const [searchQuery, setSearchQuery] = useState("");

  const title = "Topic: ";
  let topic = "US Elections";
  let time = "Fetched: 3 min ago";
  const buttonText = "Summarize Text";
  const samsumList = [
    new Samsum("1", "", `Amazon is seeking to postpone a unionization vote at a warehouse in
    Alabama and is asking federal labor authorities to reconsider a
    decision to allow mail-in voting due to the pandemic. You're telling
    me Jeff Bezos & Amazon did''nt care about the 2020 pres election
    using non-paper ballots, but now that their employees are trying to
    unionize they don't want anything other than paper ballots to
    protect the integrity of their election? Do I have this right? TNR`),
    new Samsum("2", "", `A few Antifa Twitter accounts have been suspended after ONE video of
    anti-fascist agitators destroying a democratic party building in
    Portland. The democrats and silicon valley elites were fine with
    defending anti-fascist agitators while they were destroying small
    businesses and attacking Trump supporters, Kamala Harris even
    tweeted their bail fund. Now that Biden is in office, the system has
    begun to discard their unwitting pawns in Antifa. The system never
    supported Antifa, they only used them to create chaos in Trumps
    America; and to oppose any sort of street level unity of distraught
    and angry white people. Antifa will still operate, but expect to see
    them deplatformed, cracked down on by the police, and given much
    harsher legal treatment than ever before; the system is done with
    them.`),
    new Samsum("3", "", `You just edit any text to type in the conversation you want to show,
    and delete any bubbles you don’t want to use`),
    new Samsum("4", "", `Will head to the Help Center if I have more questions tho`),

  ]

  const summarizeText = () => {
    if(selectedDialogueIndex !== -1){
      setSelectedDialogue(samsumList[selectedDialogueIndex])
      navigate('/summary');
    }
  }

  const selectDialogue = (index:number) => {
    if (selectedDialogueIndex === index) {
      setselectedDialogueIndex(-1);
  } else {
      setselectedDialogueIndex(index);
  }
  }

  return (
    <>
      <div className="api-selector">
        <ApiSelector setSelectedAPI={setSelectedAPI} />
        {isSearch ? <SearchBar setSearchQuery={setSearchQuery}/> : <></>}
      </div>
      <div className="dialogues-area">
        <div className="topic-area">
          <div className="topic-title">{title}</div>
          <div className="topic">{topic}</div>
        </div>
        <div className="fetch-time">{time}</div>
        <div className="dialogue-list">
          {samsumList.map((samsum, index)=>(
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
