import json
import os
import datetime
from typing import Dict, Any, Optional

class TicketExportConverter:
    def __init__(self, input_file: str, output_dir: str = "ticket_exports"):
        self.input_file = input_file
        self.output_dir = output_dir
        self.tickets_data = None
        
        os.makedirs(output_dir, exist_ok=True)
    
    def load_data(self) -> None:
        try:
            with open(self.input_file, 'r', encoding='utf-8') as file:
                self.tickets_data = json.load(file)
                print(f"Successfully loaded data from {self.input_file}")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading data: {e}")
            exit(1)
    
    def format_timestamp(self, timestamp: int) -> str:
        if timestamp > 10000000000:
            timestamp //= 1000
        return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    
    def process_tickets(self) -> None:
        if not self.tickets_data:
            print("No data loaded. Run load_data() first.")
            return
        
        if isinstance(self.tickets_data, list):
            for ticket in self.tickets_data:
                self.process_single_ticket(ticket)
        elif isinstance(self.tickets_data, dict):
            if "messages" in self.tickets_data or "channel" in self.tickets_data:
                self.process_single_ticket(self.tickets_data)
            else:
                for ticket_id, ticket_data in self.tickets_data.items():
                    self.process_single_ticket(ticket_data, ticket_id)
        else:
            print(f"Unknown data structure: {type(self.tickets_data)}")
    
    def process_single_ticket(self, ticket_data: Dict[str, Any], ticket_id: Optional[str] = None) -> None:
        if not isinstance(ticket_data, dict):
            print(f"Skipping invalid ticket data: {ticket_data}")
            return
        
        ticket_id = ticket_id or ticket_data.get("id") or f"ticket_{hash(str(ticket_data))}"
        
        ticket_name = self.get_ticket_name(ticket_data)
        messages = ticket_data.get("messages", [])
        
        safe_name = ''.join(c if c.isalnum() else '_' for c in ticket_name)
        output_file = os.path.join(self.output_dir, f"{safe_name}_{ticket_id}.txt")
        
        with open(output_file, 'w', encoding='utf-8') as file:
            self.write_ticket_header(file, ticket_name, ticket_id, ticket_data)
            self.write_messages(file, messages)
            
        print(f"Exported ticket '{ticket_name}' to {output_file}")
    
    def get_ticket_name(self, ticket_data: Dict[str, Any]) -> str:
        if isinstance(ticket_data, dict):
            if "channel" in ticket_data and isinstance(ticket_data["channel"], dict):
                return ticket_data["channel"].get("name", "Unknown Ticket")
            return ticket_data.get("name", "Unknown Ticket")
        return "Unknown Ticket"
    
    def write_ticket_header(self, file, ticket_name, ticket_id, ticket_data):
        file.write(f"Ticket: {ticket_name}\nID: {ticket_id}\n")
        
        if "createdAt" in ticket_data:
            file.write(f"Created: {self.format_timestamp(ticket_data['createdAt'])}\n")
        if "closedAt" in ticket_data:
            file.write(f"Closed: {self.format_timestamp(ticket_data['closedAt'])}\n")
        if "creator" in ticket_data and isinstance(ticket_data["creator"], dict):
            creator = ticket_data["creator"]
            creator_name = creator.get("username", "Unknown User")
            creator_id = creator.get("id", "Unknown ID")
            file.write(f"Created by: {creator_name} (ID: {creator_id})\n")
        
        file.write("\n" + "="*50 + "\n\n")
    
    def write_messages(self, file, messages: list):
        for msg in messages:
            if not isinstance(msg, dict):
                continue
            author = msg.get("author", {}).get("username", "Unknown User")
            author_id = msg.get("author", {}).get("id", "Unknown ID")
            content = msg.get("content", "")
            timestamp = msg.get("timestamp", 0)
            
            file.write(f"[{self.format_timestamp(timestamp)}] {author} (ID: {author_id}):\n{content}\n\n")
            
            attachments = msg.get("attachments", [])
            if attachments:
                file.write("Attachments:\n")
                for attachment in attachments:
                    if isinstance(attachment, dict):
                        url = attachment.get("url", "No URL")
                        file.write(f"- {url}\n")
                file.write("\n")
                
            file.write("-"*30 + "\n\n")

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Convert Discord Ticket Bot JSON exports to readable format')
    parser.add_argument('input_file', help='Path to the JSON export file')
    parser.add_argument('--output-dir', default='ticket_exports', help='Directory to save the converted files')
    
    args = parser.parse_args()
    
    converter = TicketExportConverter(args.input_file, args.output_dir)
    converter.load_data()
    converter.process_tickets()
    
    print(f"All tickets processed and saved to {args.output_dir}")

if __name__ == "__main__":
    main()