import { useState } from "react";
import { ApiSelectorItem } from "../ApiSelectorItem/ApiSelectorItem";
import "./ApiSelector.css";
import { APIConstants } from "../../../../constants/APIConstants";

interface ApiSelectorProps {
  setSelectedAPI: (api: APIConstants) => void;
}

export function ApiSelector(props: ApiSelectorProps) {
  const [isTwitter, setIsTwitter] = useState(false);
  const [isReddit, setIsReddit] = useState(false);
  const [isTelegram, setIsTelegram] = useState(false);

  function selectAPI(api: APIConstants) {
    setIsTwitter(false);
    setIsReddit(false);
    setIsTelegram(false);

    switch (api) {
      case APIConstants.TWITTER:
        setIsTwitter(true);
        props.setSelectedAPI(APIConstants.TWITTER);
        break;
      case APIConstants.REDDIT:
        setIsReddit(true);
        props.setSelectedAPI(APIConstants.REDDIT);
        break;
      case APIConstants.TELEGRAM:
        setIsTelegram(true);
        props.setSelectedAPI(APIConstants.TELEGRAM);
        break;
    }
  }

  return (
    <>
      <div className="api-selector-container">
        <ApiSelectorItem
          text="Twitter"
          isSelected={isTwitter}
          onClick={() => selectAPI(APIConstants.TWITTER)}
        />
        <ApiSelectorItem
          text="Reddit"
          isSelected={isReddit}
          onClick={() => selectAPI(APIConstants.REDDIT)}
        />
        <ApiSelectorItem
          text="Telegram"
          isSelected={isTelegram}
          onClick={() => selectAPI(APIConstants.TELEGRAM)}
        />
      </div>
    </>
  );
}
