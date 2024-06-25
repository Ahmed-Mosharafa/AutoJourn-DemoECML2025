import { Samsum } from "../backend-objects/Samsum";
import axios from 'axios';

const backendUrl = "http://localhost:8787";

abstract class Summary {
    conversations: Samsum[];

    constructor(conversations: Samsum[]) {
        this.conversations = conversations;
    }

    abstract getSummary(): Promise<any>;
}

export class TopicAwareSummary extends Summary {
    numOfTopics: number;

    constructor(conversations: Samsum[], numOfTopics: number) {
        super(conversations);
        this.numOfTopics = numOfTopics;
    }

    async getSummary(): Promise<any> {
        // Make a POST request to the backend API to get the summary
        let response = await axios.post(backendUrl + '/topic-aware-summarize', {
            conversation_list: this.conversations,
            numOfTopics: this.numOfTopics
        })

        return response.data.conv_summaries;
    }
}