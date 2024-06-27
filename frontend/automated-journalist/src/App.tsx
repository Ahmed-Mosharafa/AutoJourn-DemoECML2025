import { BrowserRouter, Route, Routes } from "react-router-dom";
import "./App.css";
import { Feed } from "./components/Feed/Feed";
import { Logo } from "./components/common/Logo/Logo";
import { Menu } from "./components/common/Menu/MenuLayout/Menu";
import { ApiSelector } from "./components/common/ApiSelector/ApiSelectorLayout/ApiSelector";
import { HotTopics } from "./components/common/HotTopics/HotTopicsLayout/HotTopics";
import { Summary } from "./components/Summary/Summary";
import { Settings } from "./components/Settings/Settings";
import { useState } from "react";
import { Samsum } from "./backend-objects/Samsum";

function App() {
  const [selectedDialogue, setSelectedDialogue] = useState<Samsum | null>(null);

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
            <Route path="/summary" element={<Summary selectedDialogue={selectedDialogue}/>} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </div>
      </BrowserRouter>
    </>
  );
}

export default App;
