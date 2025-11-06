import '@shopify/ui-extensions/preact';
import {render} from 'preact';
import {useState, useEffect} from 'preact/hooks';

export default function() {
  render(<SettingsExtension />, document.body);
}

function SettingsExtension() {
  const {i18n} = shopify;
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(false);
  
  const [termiiConfigured, setTermiiConfigured] = useState(false);
  const [termiiSenderId, setTermiiSenderId] = useState('');
  
  const [formData, setFormData] = useState({
    order_confirmation_template: 'Hi {{customer_name}}, your order #{{order_number}} has been confirmed. Total: {{total_price}}. Thank you!',
    fulfillment_template: 'Hi {{customer_name}}, your order #{{order_number}} has been shipped and will arrive soon!'
  });

  useEffect(() => {
    loadSettings();
  }, []);

  function getShopDomain() {
    // Priority 1: URL query parameter (most reliable for embedded apps)
    const urlParams = new URLSearchParams(window.location.search);
    let shopDomain = urlParams.get('shop');
    
    // Priority 2: App Bridge session
    if (!shopDomain && shopify?.session?.shop) {
      shopDomain = shopify.session.shop;
    }
    
    // Priority 3: Try to extract from referrer
    if (!shopDomain) {
      try {
        const referrer = document.referrer;
        const match = referrer.match(/https:\/\/([^/]+\.myshopify\.com)/);
        if (match) {
          shopDomain = match[1];
        }
      } catch (e) {
        // Ignore
      }
    }
    
    // Normalize: ensure it includes .myshopify.com
    if (shopDomain && !shopDomain.includes('.myshopify.com')) {
      shopDomain = `${shopDomain}.myshopify.com`;
    }
    
    return shopDomain;
  }

  async function loadSettings() {
    setLoading(true);
    setError(null);
    try {
      const shopDomain = getShopDomain();
      
      if (!shopDomain) {
        setError('Unable to determine shop domain. Please ensure you are accessing this from within Shopify Admin.');
        setLoading(false);
        return;
      }
      
      const response = await fetch(`/api/settings?shop=${shopDomain}`);
      
      if (response.ok) {
        const data = await response.json();
        setTermiiConfigured(data.termii_configured || false);
        setTermiiSenderId(data.termii_sender_id || '');
        setFormData({
          order_confirmation_template: data.order_confirmation_template || formData.order_confirmation_template,
          fulfillment_template: data.fulfillment_template || formData.fulfillment_template
        });
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to load settings');
      }
    } catch (err) {
      console.error('Error loading settings:', err);
      setError('Error loading settings');
    } finally {
      setLoading(false);
    }
  }

  async function saveSettings() {
    setSaving(true);
    setError(null);
    setSuccess(false);
    
    try {
      const shopDomain = getShopDomain();
      
      if (!shopDomain) {
        setError('Unable to determine shop domain. Please ensure you are accessing this from within Shopify Admin.');
        setSaving(false);
        return;
      }
      
      const response = await fetch(`/api/settings?shop=${shopDomain}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData)
      });

      if (response.ok) {
        setSuccess(true);
        // Reload settings after successful save
        await loadSettings();
        setTimeout(() => setSuccess(false), 3000);
      } else {
        const errorData = await response.json();
        setError(errorData.detail || 'Failed to save settings');
      }
    } catch (err) {
      console.error('Error saving settings:', err);
      setError('Error saving settings');
    } finally {
      setSaving(false);
    }
  }

  if (loading) {
    return (
      <s-stack gap="base">
        <s-spinner size="large" />
        <s-text>Loading settings...</s-text>
      </s-stack>
    );
  }

  return (
    <s-stack gap="large" direction="block">
      {error && (
        <s-banner tone="critical" dismissible onDismiss={() => setError(null)}>
          {error}
        </s-banner>
      )}
      
      {success && (
        <s-banner tone="success" dismissible onDismiss={() => setSuccess(false)}>
          Templates saved successfully!
        </s-banner>
      )}

      <s-section heading="Termii Configuration">
        <s-stack gap="base" direction="block">
          {termiiConfigured ? (
            <s-banner tone="success">
              <s-stack gap="tight" direction="block">
                <s-text weight="bold">Termii is configured ✓</s-text>
                <s-text>Sender ID: {termiiSenderId}</s-text>
                <s-text size="small">Termii API credentials are configured in your server's .env file.</s-text>
              </s-stack>
            </s-banner>
          ) : (
            <s-banner tone="warning">
              <s-stack gap="tight" direction="block">
                <s-text weight="bold">Termii not configured</s-text>
                <s-text size="small">Please add TERMII_API_KEY and TERMII_SENDER_ID to your server's .env file.</s-text>
              </s-stack>
            </s-banner>
          )}
        </s-stack>
      </s-section>

      <s-section heading="SMS Templates">
        <s-stack gap="base" direction="block">
          <s-text size="small" tone="subdued">
            Customize the SMS messages sent to customers. Templates are saved per-shop and persist across server restarts.
          </s-text>
          
          <s-text-area
            label="Order Confirmation Template"
            value={formData.order_confirmation_template}
            onInput={(e) => setFormData({...formData, order_confirmation_template: e.target.value})}
            rows={3}
            helpText="Available variables: {{customer_name}}, {{order_number}}, {{total_price}}"
          />
          
          <s-text-area
            label="Fulfillment Template"
            value={formData.fulfillment_template}
            onInput={(e) => setFormData({...formData, fulfillment_template: e.target.value})}
            rows={3}
            helpText="Available variables: {{customer_name}}, {{order_number}}"
          />
        </s-stack>
      </s-section>

      <s-button
        variant="primary"
        loading={saving}
        onClick={saveSettings}
        slot="primary-action"
      >
        Save Templates
      </s-button>
    </s-stack>
  );
}
