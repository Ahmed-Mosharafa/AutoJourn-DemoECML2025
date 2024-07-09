import { BrowserRouter, Route, Routes } from "react-router-dom";
import "./App.css";
import { Feed } from "./components/Feed/Feed";
import { Logo } from "./components/common/Logo/Logo";
import { Menu } from "./components/common/Menu/MenuLayout/Menu";
import { HotTopics } from "./components/common/HotTopics/HotTopicsLayout/HotTopics";
import { Summary } from "./components/Summary/Summary";
import { Settings } from "./components/Settings/Settings";
import { useState } from "react";
import { Samsum } from "./backend-objects/Samsum";
import {CompareSummaries} from "./components/CompareSummaries/CompareSummaries";

function App() {
  const [selectedDialogue, setSelectedDialogue] = useState<Samsum | null>(null);

  const [selectedCompareTopic1, setSelectedCompareTopic1] = useState('');
  const [selectedCompareTopic2, setSelectedCompareTopic2] = useState('');

  return (
    <>
      <BrowserRouter>
        <div className="left-layout">
          <Logo />
          <Menu />
        </div>
        <div className="right-layout">
          <HotTopics />
        </div>
        <div className="content">
          <Routes>
            <Route path="/" element={<Feed setSelectedDialogue={setSelectedDialogue} />} />
            <Route path="/feed" element={<Feed setSelectedDialogue={setSelectedDialogue} />} />
            <Route path="/search" element={<Feed setSelectedDialogue={setSelectedDialogue} isSearch={true}/>} />
            <Route path="/summary" element={<Summary selectedDialogue={selectedDialogue} selectedCompareTopic1={selectedCompareTopic1} selectedCompareTopic2={selectedCompareTopic2} setSelectedCompareTopic1={setSelectedCompareTopic1} setSelectedCompareTopic2={setSelectedCompareTopic2}/>} />
            <Route path="/compare-summaries" element={<CompareSummaries selectedCompareTopic1={selectedCompareTopic1} selectedCompareTopic2={selectedCompareTopic2} />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </div>
      </BrowserRouter>
    </>
  );
}

export default App;
