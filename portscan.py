import dearpygui.dearpygui as dpg
import sys
import socket



def quit():
    print("Exiting...")
    sys.exit()

def scan(sender, app_data, user_data):
    port_list = user_data
    if len(port_list) > 0:
        port_list.clear()

    dpg.configure_item("##port_list", items=port_list)
    dpg.configure_item("##scan_btn", enabled=False)
    
    low_port = dpg.get_value("low_port")
    high_port = dpg.get_value("high_port")
    ip_address = dpg.get_value("ip_address")
    
    print(f"Scanning {ip_address} for open ports.\n")
    for port in range(low_port, high_port):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sckt:
                sckt.settimeout(0.5)
                result = sckt.connect_ex((ip_address, port))
                if result == 0:
                    port_list.append(f"Port {port} open!")
                    dpg.configure_item('##port_list', items=port_list)
                else:
                    pass
        except KeyboardInterrupt:
            print('\nExiting..')
            sys.exit()
        except socket.gaierror:
            print('Hostname could not be resolved')
            sys.exit()
        except socket.timeout:
            print('Connection timed out. Took too long to get a response. ')
            sys.exit()
        except socket.error:
            print("Couldn't connect to server.")
            sys.exit()
            
        dpg.set_value("##Progress_Bar", (port/high_port))
        dpg.configure_item("##Progress_Bar", overlay=f"{port} / {round((port/high_port)*100)}%")
                
            
    print("Scan complete")
    dpg.configure_item('##Progress_Bar', overlay="Scan Complete")
    dpg.configure_item('##scan_btn', enabled=True)

def main():
    dpg.create_context()
    port_list = []

    with dpg.value_registry():
        dpg.add_string_value(default_value="127.0.0.1", tag='ip_address')
        dpg.add_int_value(default_value=0, tag="low_port")
        dpg.add_int_value(default_value=65535, tag="high_port")

    with dpg.window(tag="Primary Window"):
        with dpg.menu_bar():
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="Quit", callback=quit)
        dpg.add_input_text(label="IPAddress", source="ip_address")
        with dpg.group(horizontal=True):
            dpg.add_slider_int(default_value=0, min_value=0, max_value=65535, source='low_port', clamped=True, width=200)
            dpg.add_slider_int(default_value=65535, min_value=0, max_value=65535, source='high_port', clamped=True, width=200)
        
        dpg.add_button(label="Scan", callback=scan, tag="##scan_btn", user_data=port_list)

        dpg.add_listbox(label="##port_list", tag="##port_list", num_items=10)
        dpg.add_progress_bar(label="##Progress_Bar", default_value=0, tag='##Progress_Bar')

    dpg.create_viewport(title="PortScan", width=500, height=325)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("Primary Window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == "__main__":
    main()