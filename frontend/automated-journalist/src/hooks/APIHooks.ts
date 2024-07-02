import { useEffect, useState } from "react";
import { Telegram } from "../api/SocialAPI";
import { Samsum } from "../backend-objects/Samsum";
import { ConversationSummary } from "../api/Summary";
import useStore from "../store/store";

export const useFetchTelegramSearch = () => {
    const { searchQuery, setConversations } = useStore();
    const [data, setData] = useState<[Samsum] | null>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            if (searchQuery === "" || searchQuery === null) {
                setLoading(false);
                setData(null);
                setError(null);
                return;
            }
            try {
                const teleAPI = new Telegram();
                const data = await teleAPI.getFeedData(searchQuery);
                setData(data);
                setConversations(data);
                setLoading(false);
            } catch (error) {
                setError("Error fetching data");
                setLoading(false);
            }
        }

        fetchData();
    }, [searchQuery]);

    return { data, loading, error };
}

export const useSummarize = (conversations: Samsum[]) => {
    const { searchQuery,setIsSummarize } = useStore()
    const [summary, setSummary] = useState<[Samsum] | null>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);
    const fetchSummary = async () => {
        setLoading(true);
        setError(null);
        try {
            const summaryAPI = new ConversationSummary(conversations)
            const summary = await summaryAPI.getSummary();
            setSummary(summary);
            // Set isSummarize false after summary is performed.
            setIsSummarize(false);
        } catch (err) {
            setError('Error fetching summary');
        } finally {
            setLoading(false);
        }
    };

    return { fetchSummary, summary, loading, error };
}