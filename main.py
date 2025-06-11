(async function() {
    // Prevent re-execution
    if (window.__otpFetched) return;
    window.__otpFetched = true;

    try {
        // Fetch OTP from your API
        const response = await fetch("https://otp-service-elig.onrender.com/generate-otp", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                "master_key": "SZJLKA2HXHVXALFD72OOFHJNZBKOVNGO"
            })
        });

        const data = await response.json();
        const otp = data.otp;

        console.log("✅ Fetched OTP:", otp);

        // Wait for the OTP input field to be available (max 10s)
        const waitForInput = async (selector, timeout = 10000) => {
            const interval = 200;
            const maxTries = timeout / interval;
            let attempts = 0;
            return new Promise((resolve, reject) => {
                const timer = setInterval(() => {
                    const el = document.querySelector(selector);
                    if (el) {
                        clearInterval(timer);
                        resolve(el);
                    } else if (++attempts >= maxTries) {
                        clearInterval(timer);
                        reject(new Error("❌ OTP input field not found within timeout"));
                    }
                }, interval);
            });
        };

        // Try multiple selectors based on common PingID implementations
        const otpInput = await waitForInput('input[type="text"], input[autocomplete="one-time-code"], input');

        // Insert the OTP and trigger input event
        otpInput.value = otp;
        otpInput.dispatchEvent(new Event('input', { bubbles: true }));

        console.log("✅ OTP inserted into input field");

    } catch (error) {
        console.error("❌ Error during OTP fetch or entry:", error);
    }
})();
