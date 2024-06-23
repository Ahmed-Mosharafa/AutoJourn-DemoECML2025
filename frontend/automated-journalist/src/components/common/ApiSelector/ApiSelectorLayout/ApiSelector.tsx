import { useState } from "react";
import { ApiSelectorItem } from "../ApiSelectorItem/ApiSelectorItem";
import "./ApiSelector.css";
import { API } from "../../../../api/APIEnums";

interface ApiSelectorProps {
  setSelectedAPI: (api: API) => void;
}

export function ApiSelector(props: ApiSelectorProps) {
  const [isTwitter, setIsTwitter] = useState(false);
  const [isReddit, setIsReddit] = useState(false);
  const [isTelegram, setIsTelegram] = useState(false);

  function selectAPI(api: string) {
    setIsTwitter(false);
    setIsReddit(false);
    setIsTelegram(false);

    switch (api) {
      case API.TWITTER:
        setIsTwitter(true);
        props.setSelectedAPI(API.TWITTER);
        break;
      case API.REDDIT:
        setIsReddit(true);
        props.setSelectedAPI(API.REDDIT);
        break;
      case API.TELEGRAM:
        setIsTelegram(true);
        props.setSelectedAPI(API.TELEGRAM);
        break;
    }
  }

  return (
    <>
      <div className="api-selector-container">
        <ApiSelectorItem
          text="Twitter"
          isSelected={isTwitter}
          onClick={() => selectAPI(API.TWITTER)}
        />
        <ApiSelectorItem
          text="Reddit"
          isSelected={isReddit}
          onClick={() => selectAPI(API.REDDIT)}
        />
        <ApiSelectorItem
          text="Telegram"
          isSelected={isTelegram}
          onClick={() => selectAPI(API.TELEGRAM)}
        />
      </div>
    </>
  );
}
