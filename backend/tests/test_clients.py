from backend.clients.supabase_client import SupabaseRESTClient
from backend.clients.traccar_client import TraccarGatewayClient
from backend.clients.maps_client import UnifiedMapsClient

def test_clients_init():
    sb = SupabaseRESTClient("https://mock.supabase.co", "key123")
    assert sb.get_headers()["apikey"] == "key123"
    
    tc = TraccarGatewayClient("http://traccar.local")
    url = tc.format_position_url("dev01", 12.97, 77.59)
    assert "dev01" in url
    
    mc = UnifiedMapsClient("g_key", "o_key")
    assert mc.is_configured() is True
