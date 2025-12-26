export async function fetcher(endpoint: string, token: string) {
    try {
        const res = await fetch(endpoint, {
            headers: {
                Authorization: `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
        });

        const text = await res.text();
        if (!res.ok) {
            console.error('Response body:', text);
            throw new Error(`HTTP ${res.status} - ${res.statusText}`);
        }

        return JSON.parse(text);
    } catch (err) {
        console.error('Fetch error:', err);
        throw err; // propagate to caller
    }
}
