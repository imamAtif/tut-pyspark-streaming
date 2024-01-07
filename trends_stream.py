import time
from datetime import datetime
from pytrends.request import TrendReq
import socket
import atexit


def send_message(message):
    server_address = ("127.0.0.1", 5555)

    # Create a socket and connect to the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect(server_address)

        # Send a message to the server continuously
        client_socket.sendall(message.encode("utf-8"))


def get_trends():
    pytrends = TrendReq(hl="en-us")
    kw_list = ["football"]

    # Set the timeframe to the past 1 hour
    pytrends.build_payload(kw_list, cat=0, timeframe="now 1-H")

    # Infinite loop for continuous streaming
    while True:
        try:
            # Fetch related queries for the specified keyword
            data = pytrends.related_queries()

            # Print the data along with the current time
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Extract and print the search terms for India
            keyword = kw_list[0]
            related_queries = (
                data[keyword]["top"]
                if data[keyword] and "top" in data[keyword]
                else {"query": []}
            )
            search_terms = related_queries.get("query", [])
            search_terms_str = ", ".join(search_terms)

            # Send the data to the socket
            output = f"{current_time} {search_terms_str}\n"
            print(output)
            send_message(output)
        except KeyboardInterrupt:
            print("\nScript manually interrupted. Exiting.")
            break
        except Exception as e:
            print(f"Error: {e}")

        # Wait for the specified delay before the next iteration
        time.sleep(10)


if __name__ == "__main__":
    get_trends()
