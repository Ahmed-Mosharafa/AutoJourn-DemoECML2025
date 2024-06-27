import { useEffect, useState } from "react";
import { Telegram } from "../api/SocialAPI";
import { Samsum } from "../backend-objects/Samsum";

export const useFetchTelegramSearch = (query: string) => {
    const [data, setData] = useState<[Samsum] | null>(null);
    const [loading, setLoading] = useState<boolean>(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchData = async () => {
            if (query === "" || query === null) {  
                setLoading(false);
                setData(null);
                setError(null);
                return;
            }
                try {
                const teleAPI = new Telegram();
                const data = await teleAPI.getFeedData(query);
                setData(data);
                setLoading(false);
            } catch (error) {
                setError("Error fetching data");
                setLoading(false);
            }
        }

        fetchData();
    }, [query]);

    return { data, loading, error};
}