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

export class ConversationSummary extends Summary {
    constructor(conversations: Samsum[]) {
        super(conversations);
    }

    async getSummary(): Promise<any> {
        let response = await axios.post(backendUrl + '/summarize', {
            conversations: this.conversations
        })

        return response.data.summaries;
    }
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
            conversations: this.conversations,
            num_topics: this.numOfTopics
        })

        return response.data.conv_summaries;
    }
}