import { BrowserRouter, Route, Routes } from "react-router-dom";
import "./App.css";
import { Feed } from "./components/Feed/Feed";
import { Logo } from "./components/common/Logo/Logo";
import { Menu } from "./components/common/Menu/MenuLayout/Menu";
import { ApiSelector } from "./components/common/ApiSelector/ApiSelectorLayout/ApiSelector";
import { HotTopics } from "./components/common/HotTopics/HotTopicsLayout/HotTopics";
import { Summary } from "./components/Summary/Summary";

function App() {
  return (
    <>
      <div className="left-layout">
        <Logo />
        <Menu />
      </div>
      <div className="center-layout">
        <ApiSelector />
      </div>
      <div className="right-layout">
        <HotTopics />
      </div>
      <div className="content">
        <BrowserRouter>
          <Routes>
            <Route path="/" element={<Feed />} />
            <Route path="/feed" element={<Feed />} />
            <Route path="/summary" element={<Summary />} />
          </Routes>
        </BrowserRouter>
      </div>
    </>
  );
}

export default App;
