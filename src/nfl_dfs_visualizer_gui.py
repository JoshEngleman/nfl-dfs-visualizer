#!/usr/bin/env python3
"""
NFL DFS Visualizer - GUI Application
Easy-to-use graphical interface for creating DFS visualizations
with name matching support
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import sys
import os
from pathlib import Path
import threading
import json

# Import the visualizer
from nfl_dfs_visualizer import NFLDFSVisualizer


class NameMatchingDialog:
    """Dialog for managing player name mappings"""

    def __init__(self, parent, visualizer, unmatched_names, mappings_file):
        self.visualizer = visualizer
        self.unmatched_names = unmatched_names
        self.mappings_file = mappings_file
        self.mappings = {}

        # Load existing mappings
        self.load_mappings()

        # Create dialog window
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Player Name Matching")
        self.dialog.geometry("900x600")
        self.dialog.resizable(True, True)

        self.setup_ui()

    def load_mappings(self):
        """Load existing mappings from file"""
        if os.path.exists(self.mappings_file):
            try:
                with open(self.mappings_file, 'r') as f:
                    data = json.load(f)
                    self.mappings = data.get('mappings', {})
            except Exception as e:
                print(f"Error loading mappings: {e}")
                self.mappings = {}

    def save_mappings(self):
        """Save mappings to file"""
        try:
            with open(self.mappings_file, 'w') as f:
                json.dump({
                    'mappings': self.mappings,
                    'notes': 'This file stores manual player name mappings from CSV to NFL roster data'
                }, f, indent=2)
            messagebox.showinfo("Success", f"Saved {len(self.mappings)} name mappings")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save mappings:\n{e}")

    def setup_ui(self):
        """Create the UI for name matching"""
        # Main container
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.dialog.columnconfigure(0, weight=1)
        self.dialog.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        # Title and instructions
        title_frame = ttk.Frame(main_frame)
        title_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))

        title = ttk.Label(
            title_frame,
            text="Unmatched Player Names",
            font=('Helvetica', 14, 'bold')
        )
        title.pack(anchor=tk.W)

        instructions = ttk.Label(
            title_frame,
            text="These players from your CSV couldn't be automatically matched to NFL roster data.\n"
                 "Select a suggested match or manually enter the correct NFL roster name.",
            font=('Helvetica', 9)
        )
        instructions.pack(anchor=tk.W, pady=(5, 0))

        # Unmatched players list
        list_frame = ttk.Frame(main_frame)
        list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        # Create treeview for unmatched names
        columns = ('csv_name', 'team', 'position', 'mapped_to', 'status')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)

        self.tree.heading('csv_name', text='CSV Name')
        self.tree.heading('team', text='Team')
        self.tree.heading('position', text='Position')
        self.tree.heading('mapped_to', text='Mapped To')
        self.tree.heading('status', text='Status')

        self.tree.column('csv_name', width=200)
        self.tree.column('team', width=80)
        self.tree.column('position', width=80)
        self.tree.column('mapped_to', width=200)
        self.tree.column('status', width=100)

        # Scrollbars
        vsb = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(list_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        vsb.grid(row=0, column=1, sticky=(tk.N, tk.S))
        hsb.grid(row=1, column=0, sticky=(tk.W, tk.E))

        # Populate tree
        self.populate_tree()

        # Bind selection event
        self.tree.bind('<<TreeviewSelect>>', self.on_select)

        # Matching panel
        match_frame = ttk.LabelFrame(main_frame, text="Match Player", padding="10")
        match_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        match_frame.columnconfigure(1, weight=1)

        # Selected player info
        self.selected_label = ttk.Label(match_frame, text="Select a player above to match",
                                       font=('Helvetica', 10, 'bold'))
        self.selected_label.grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 10))

        # Suggested matches
        ttk.Label(match_frame, text="Suggested Matches:").grid(row=1, column=0, sticky=tk.W, pady=5)

        self.suggestions_combo = ttk.Combobox(match_frame, state='readonly', width=40)
        self.suggestions_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        use_suggestion_btn = ttk.Button(match_frame, text="Use This Match",
                                       command=self.use_suggestion)
        use_suggestion_btn.grid(row=1, column=2, padx=5, pady=5)

        # Manual entry
        ttk.Label(match_frame, text="Or Enter Manually:").grid(row=2, column=0, sticky=tk.W, pady=5)

        self.manual_entry = ttk.Entry(match_frame, width=40)
        self.manual_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        use_manual_btn = ttk.Button(match_frame, text="Use Manual Entry",
                                    command=self.use_manual)
        use_manual_btn.grid(row=2, column=2, padx=5, pady=5)

        # Clear mapping button
        clear_btn = ttk.Button(match_frame, text="Clear Mapping",
                              command=self.clear_mapping)
        clear_btn.grid(row=3, column=1, sticky=tk.W, padx=5, pady=5)

        # Bottom buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, sticky=(tk.E), pady=(10, 0))

        save_btn = ttk.Button(button_frame, text="Save Mappings",
                             command=self.save_and_close, style='Accent.TButton')
        save_btn.pack(side=tk.RIGHT, padx=(5, 0))

        close_btn = ttk.Button(button_frame, text="Close", command=self.dialog.destroy)
        close_btn.pack(side=tk.RIGHT)

    def populate_tree(self):
        """Populate the tree with unmatched names"""
        self.tree.delete(*self.tree.get_children())

        for player in self.unmatched_names:
            name = player['name']
            team = player['team']
            position = player.get('position', 'Unknown')

            mapping_key = f"{name}|{team}"
            mapped_to = self.mappings.get(mapping_key, '')
            status = 'Mapped' if mapped_to else 'Unmatched'

            self.tree.insert('', tk.END, values=(name, team, position, mapped_to, status))

    def on_select(self, event):
        """Handle player selection"""
        selection = self.tree.selection()
        if not selection:
            return

        item = self.tree.item(selection[0])
        values = item['values']
        name, team, position = values[0], values[1], values[2]

        self.selected_label.config(text=f"Matching: {name} ({team} - {position})")

        # Find potential matches
        self.current_name = name
        self.current_team = team

        potential_matches = self.visualizer.find_potential_matches(name, team, limit=20)

        # Populate suggestions
        suggestions = []
        for match in potential_matches:
            suggestions.append(f"{match['player_name']} ({match['team']} - {match['position']})")

        self.suggestions_combo['values'] = suggestions if suggestions else ['No suggestions found']
        if suggestions:
            self.suggestions_combo.current(0)

        # Set manual entry to current mapping if exists
        mapping_key = f"{name}|{team}"
        current_mapping = self.mappings.get(mapping_key, '')
        self.manual_entry.delete(0, tk.END)
        self.manual_entry.insert(0, current_mapping)

    def use_suggestion(self):
        """Use the selected suggestion"""
        selection = self.suggestions_combo.get()
        if not selection or selection == 'No suggestions found':
            messagebox.showwarning("No Selection", "Please select a suggested match")
            return

        # Extract player name from suggestion (format: "Name (TEAM - POS)")
        nfl_name = selection.split(' (')[0]

        mapping_key = f"{self.current_name}|{self.current_team}"
        self.mappings[mapping_key] = nfl_name

        self.populate_tree()
        messagebox.showinfo("Success", f"Mapped '{self.current_name}' to '{nfl_name}'")

    def use_manual(self):
        """Use the manual entry"""
        nfl_name = self.manual_entry.get().strip()
        if not nfl_name:
            messagebox.showwarning("Empty Entry", "Please enter an NFL roster name")
            return

        mapping_key = f"{self.current_name}|{self.current_team}"
        self.mappings[mapping_key] = nfl_name

        self.populate_tree()
        messagebox.showinfo("Success", f"Mapped '{self.current_name}' to '{nfl_name}'")

    def clear_mapping(self):
        """Clear the current mapping"""
        if not hasattr(self, 'current_name'):
            messagebox.showwarning("No Selection", "Please select a player first")
            return

        mapping_key = f"{self.current_name}|{self.current_team}"
        if mapping_key in self.mappings:
            del self.mappings[mapping_key]
            self.populate_tree()
            messagebox.showinfo("Cleared", f"Cleared mapping for '{self.current_name}'")
        else:
            messagebox.showinfo("No Mapping", "No mapping exists for this player")

    def save_and_close(self):
        """Save mappings and close dialog"""
        self.save_mappings()
        self.dialog.destroy()


class NFLDFSVisualizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NFL DFS Boom/Bust Visualizer")
        self.root.geometry("600x550")
        self.root.resizable(True, True)

        # Variables
        self.csv_path = tk.StringVar()
        self.output_path = tk.StringVar(value="boom_bust.html")
        self.position = tk.StringVar(value="ALL")
        self.status_text = tk.StringVar(value="Ready to generate visualization")
        self.mappings_file = Path('name_mappings.json')
        self.name_mappings = {}

        # Load existing mappings
        self.load_mappings()

        # Configure style
        style = ttk.Style()
        style.theme_use('default')

        self.setup_ui()

    def load_mappings(self):
        """Load name mappings from file"""
        if self.mappings_file.exists():
            try:
                with open(self.mappings_file, 'r') as f:
                    data = json.load(f)
                    self.name_mappings = data.get('mappings', {})
            except Exception as e:
                print(f"Error loading mappings: {e}")
                self.name_mappings = {}

    def setup_ui(self):
        """Create the GUI layout"""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configure grid weights for responsiveness
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

        # Title
        title = ttk.Label(
            main_frame,
            text="NFL DFS Boom/Bust Visualizer",
            font=('Helvetica', 18, 'bold')
        )
        title.grid(row=0, column=0, columnspan=3, pady=(0, 20))

        # Description
        desc = ttk.Label(
            main_frame,
            text="Generate interactive HTML visualizations from your DFS CSV data",
            font=('Helvetica', 10)
        )
        desc.grid(row=1, column=0, columnspan=3, pady=(0, 20))

        # CSV File Selection
        csv_label = ttk.Label(main_frame, text="CSV File:", font=('Helvetica', 10, 'bold'))
        csv_label.grid(row=2, column=0, sticky=tk.W, pady=5)

        csv_entry = ttk.Entry(main_frame, textvariable=self.csv_path, width=40)
        csv_entry.grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)

        csv_button = ttk.Button(main_frame, text="Browse...", command=self.browse_csv)
        csv_button.grid(row=2, column=2, sticky=tk.W, pady=5)

        # Output File
        output_label = ttk.Label(main_frame, text="Output File:", font=('Helvetica', 10, 'bold'))
        output_label.grid(row=3, column=0, sticky=tk.W, pady=5)

        output_entry = ttk.Entry(main_frame, textvariable=self.output_path, width=40)
        output_entry.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5, padx=5)

        output_button = ttk.Button(main_frame, text="Browse...", command=self.browse_output)
        output_button.grid(row=3, column=2, sticky=tk.W, pady=5)

        # Position Filter
        position_label = ttk.Label(main_frame, text="Position:", font=('Helvetica', 10, 'bold'))
        position_label.grid(row=4, column=0, sticky=tk.W, pady=5)

        positions = ['ALL', 'QB', 'RB', 'WR', 'TE', 'DST']
        position_combo = ttk.Combobox(
            main_frame,
            textvariable=self.position,
            values=positions,
            state='readonly',
            width=15
        )
        position_combo.grid(row=4, column=1, sticky=tk.W, pady=5, padx=5)

        # Name Matching Button
        name_match_button = ttk.Button(
            main_frame,
            text="Check Name Matches",
            command=self.check_name_matches,
            style='Accent.TButton'
        )
        name_match_button.grid(row=5, column=0, columnspan=3, pady=10)

        # Generate Button
        generate_button = ttk.Button(
            main_frame,
            text="Generate Visualization",
            command=self.generate_visualization,
            style='Accent.TButton'
        )
        generate_button.grid(row=6, column=0, columnspan=3, pady=10)

        # Progress Bar
        self.progress = ttk.Progressbar(
            main_frame,
            mode='indeterminate',
            length=400
        )
        self.progress.grid(row=7, column=0, columnspan=3, pady=10)

        # Status Label
        status_label = ttk.Label(
            main_frame,
            textvariable=self.status_text,
            font=('Helvetica', 9),
            foreground='gray'
        )
        status_label.grid(row=8, column=0, columnspan=3, pady=5)

        # Log Text Area
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="10")
        log_frame.grid(row=9, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        main_frame.rowconfigure(9, weight=1)

        # Text widget with scrollbar
        self.log_text = tk.Text(log_frame, height=10, width=70, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)

        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)

        # Add some helpful starting text
        self.log("Welcome! Select a CSV file to begin.")
        self.log("Use 'Check Name Matches' to resolve any player name mismatches.")
        self.log(f"Loaded {len(self.name_mappings)} existing name mappings.")

    def browse_csv(self):
        """Open file browser for CSV selection"""
        filename = filedialog.askopenfilename(
            title="Select CSV File",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if filename:
            self.csv_path.set(filename)
            # Auto-set output filename based on CSV location
            csv_dir = os.path.dirname(filename)
            output_file = os.path.join(csv_dir, "boom_bust.html")
            self.output_path.set(output_file)
            self.log(f"Selected CSV: {filename}")

    def browse_output(self):
        """Open file browser for output file selection"""
        filename = filedialog.asksaveasfilename(
            title="Save Visualization As",
            defaultextension=".html",
            filetypes=[("HTML files", "*.html"), ("All files", "*.*")]
        )
        if filename:
            self.output_path.set(filename)
            self.log(f"Output will be saved to: {filename}")

    def log(self, message):
        """Add message to log area"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def check_name_matches(self):
        """Check for unmatched player names"""
        csv = self.csv_path.get()

        if not csv:
            messagebox.showerror("Error", "Please select a CSV file first")
            return

        if not os.path.exists(csv):
            messagebox.showerror("Error", f"CSV file not found: {csv}")
            return

        # Run in thread
        thread = threading.Thread(target=self._check_name_matches_thread, args=(csv,))
        thread.daemon = True
        thread.start()

    def _check_name_matches_thread(self, csv):
        """Thread worker for checking name matches"""
        try:
            self.progress.start(10)
            self.status_text.set("Analyzing player names...")
            self.log("\n" + "="*50)
            self.log("Checking player name matches...")
            self.log("="*50 + "\n")

            # Reload mappings
            self.load_mappings()

            # Create visualizer to check names
            visualizer = NFLDFSVisualizer(csv, self.name_mappings)

            # Process data to find unmatched names
            positions = ['ALL'] + sorted(visualizer.df['Position'].unique().tolist())
            for pos in positions:
                visualizer.prepare_data_for_position(pos)

            unmatched = visualizer.unmatched_names

            self.log(f"Found {len(unmatched)} unmatched player names")

            if unmatched:
                # Open name matching dialog
                self.root.after(0, lambda: self._open_name_matching_dialog(visualizer, unmatched))
            else:
                self.status_text.set("All player names matched successfully!")
                self.log("✓ All player names matched successfully!")
                self.root.after(0, lambda: messagebox.showinfo(
                    "Success",
                    "All player names from your CSV were successfully matched to NFL roster data!"
                ))

        except Exception as e:
            self.status_text.set("Error checking names")
            self.log(f"\n❌ ERROR: {str(e)}")
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to check names:\n\n{str(e)}"))
        finally:
            self.progress.stop()

    def _open_name_matching_dialog(self, visualizer, unmatched_names):
        """Open the name matching dialog"""
        dialog = NameMatchingDialog(self.root, visualizer, unmatched_names, self.mappings_file)
        self.root.wait_window(dialog.dialog)

        # Reload mappings after dialog closes
        self.load_mappings()
        self.log(f"Name mappings updated. Total mappings: {len(self.name_mappings)}")

    def generate_visualization(self):
        """Generate the visualization (run in thread to prevent UI freezing)"""
        csv = self.csv_path.get()
        output = self.output_path.get()
        pos = self.position.get()

        # Validation
        if not csv:
            messagebox.showerror("Error", "Please select a CSV file")
            return

        if not os.path.exists(csv):
            messagebox.showerror("Error", f"CSV file not found: {csv}")
            return

        if not output:
            messagebox.showerror("Error", "Please specify an output file")
            return

        # Run in thread to prevent UI freezing
        thread = threading.Thread(target=self._generate_visualization_thread, args=(csv, output, pos))
        thread.daemon = True
        thread.start()

    def _generate_visualization_thread(self, csv, output, pos):
        """Thread worker for generating visualization"""
        try:
            # Update UI
            self.progress.start(10)
            self.status_text.set("Generating visualization...")
            self.log("\n" + "="*50)
            self.log("Starting visualization generation...")
            self.log(f"CSV: {csv}")
            self.log(f"Output: {output}")
            self.log(f"Position: {pos}")
            self.log(f"Using {len(self.name_mappings)} custom name mappings")
            self.log("="*50 + "\n")

            # Redirect print statements to log
            original_print = print

            def gui_print(*args, **kwargs):
                message = ' '.join(str(arg) for arg in args)
                self.log(message)

            # Temporarily replace print
            import builtins
            builtins.print = gui_print

            try:
                # Reload mappings before generating
                self.load_mappings()

                # Generate visualization with mappings
                visualizer = NFLDFSVisualizer(csv, self.name_mappings)
                visualizer.create_visualization(pos, output)

                # Success
                self.status_text.set("✓ Visualization generated successfully!")
                self.log("\n" + "="*50)
                self.log("SUCCESS! Visualization generated.")
                self.log(f"File saved to: {output}")

                # Report any unmatched names
                if visualizer.unmatched_names:
                    self.log(f"\nNote: {len(visualizer.unmatched_names)} players still unmatched (using team logos)")
                    self.log("Use 'Check Name Matches' to map these players")

                self.log("="*50)

                # Ask if user wants to open the file
                self.root.after(0, lambda: self._ask_open_file(output))

            finally:
                # Restore original print
                builtins.print = original_print

        except Exception as e:
            self.status_text.set("Error generating visualization")
            self.log(f"\n❌ ERROR: {str(e)}")
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to generate visualization:\n\n{str(e)}"))

        finally:
            self.progress.stop()

    def _ask_open_file(self, output):
        """Ask user if they want to open the generated file"""
        result = messagebox.askyesno(
            "Success",
            f"Visualization generated successfully!\n\nOpen {os.path.basename(output)} in your browser?",
            icon='info'
        )
        if result:
            self.open_file(output)

    def open_file(self, filepath):
        """Open file in default application"""
        try:
            if sys.platform == 'darwin':  # macOS
                os.system(f'open "{filepath}"')
            elif sys.platform == 'win32':  # Windows
                os.startfile(filepath)
            else:  # Linux
                os.system(f'xdg-open "{filepath}"')
        except Exception as e:
            self.log(f"Could not open file automatically: {e}")
            messagebox.showinfo("File Saved", f"Visualization saved to:\n{filepath}\n\nPlease open it manually.")


def main():
    """Main entry point"""
    root = tk.Tk()
    app = NFLDFSVisualizerGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
