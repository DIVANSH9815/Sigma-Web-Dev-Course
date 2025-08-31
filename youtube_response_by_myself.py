import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
from datetime import datetime

class YouTubeManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Manager")
        self.root.geometry("900x600")
        self.root.configure(bg="#f0f0f0")
        
        # Data storage
        self.videos = []
        self.playlists = []
        self.load_data()
        
        # Setup the GUI
        self.setup_gui()
        
    def setup_gui(self):
        # Create notebook for tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        # Create frames for each tab
        self.video_frame = ttk.Frame(self.notebook)
        self.playlist_frame = ttk.Frame(self.notebook)
        self.channel_frame = ttk.Frame(self.notebook)
        self.search_frame = ttk.Frame(self.notebook)
        
        self.notebook.add(self.video_frame, text="Videos")
        self.notebook.add(self.playlist_frame, text="Playlists")
        self.notebook.add(self.channel_frame, text="Channel Stats")
        self.notebook.add(self.search_frame, text="Search")
        
        # Setup each tab
        self.setup_video_tab()
        self.setup_playlist_tab()
        self.setup_channel_tab()
        self.setup_search_tab()
        
    def setup_video_tab(self):
        # Video list frame
        list_frame = ttk.LabelFrame(self.video_frame, text="Video List")
        list_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        # Treeview for videos
        columns = ("id", "title", "views", "likes", "date")
        self.video_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # Define headings
        self.video_tree.heading("id", text="ID")
        self.video_tree.heading("title", text="Title")
        self.video_tree.heading("views", text="Views")
        self.video_tree.heading("likes", text="Likes")
        self.video_tree.heading("date", text="Upload Date")
        
        # Define columns
        self.video_tree.column("id", width=50, anchor=tk.CENTER)
        self.video_tree.column("title", width=200, anchor=tk.W)
        self.video_tree.column("views", width=80, anchor=tk.CENTER)
        self.video_tree.column("likes", width=80, anchor=tk.CENTER)
        self.video_tree.column("date", width=100, anchor=tk.CENTER)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.video_tree.yview)
        self.video_tree.configure(yscrollcommand=scrollbar.set)
        
        self.video_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection
        self.video_tree.bind("<<TreeviewSelect>>", self.on_video_select)
        
        # Button frame
        btn_frame = ttk.Frame(self.video_frame)
        btn_frame.pack(padx=10, pady=5, fill=tk.X)
        
        ttk.Button(btn_frame, text="Add Video", command=self.add_video).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Edit Video", command=self.edit_video).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Video", command=self.delete_video).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Refresh", command=self.refresh_videos).pack(side=tk.LEFT, padx=5)
        
        # Video details frame
        self.detail_frame = ttk.LabelFrame(self.video_frame, text="Video Details")
        self.detail_frame.pack(padx=10, pady=5, fill=tk.X)
        
        # Populate video list
        self.refresh_videos()
        
    def setup_playlist_tab(self):
        # Playlist list frame
        list_frame = ttk.LabelFrame(self.playlist_frame, text="Playlists")
        list_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        # Treeview for playlists
        columns = ("id", "name", "video_count", "created_date")
        self.playlist_tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        # Define headings
        self.playlist_tree.heading("id", text="ID")
        self.playlist_tree.heading("name", text="Name")
        self.playlist_tree.heading("video_count", text="Videos")
        self.playlist_tree.heading("created_date", text="Created Date")
        
        # Define columns
        self.playlist_tree.column("id", width=50, anchor=tk.CENTER)
        self.playlist_tree.column("name", width=200, anchor=tk.W)
        self.playlist_tree.column("video_count", width=80, anchor=tk.CENTER)
        self.playlist_tree.column("created_date", width=100, anchor=tk.CENTER)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.playlist_tree.yview)
        self.playlist_tree.configure(yscrollcommand=scrollbar.set)
        
        self.playlist_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Button frame
        btn_frame = ttk.Frame(self.playlist_frame)
        btn_frame.pack(padx=10, pady=5, fill=tk.X)
        
        ttk.Button(btn_frame, text="Add Playlist", command=self.add_playlist).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Edit Playlist", command=self.edit_playlist).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Delete Playlist", command=self.delete_playlist).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="View Playlist", command=self.view_playlist).pack(side=tk.LEFT, padx=5)
        
        # Populate playlist list
        self.refresh_playlists()
        
    def setup_channel_tab(self):
        # Channel statistics frame
        stats_frame = ttk.LabelFrame(self.channel_frame, text="Channel Statistics")
        stats_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        # Statistics labels
        ttk.Label(stats_frame, text="Total Videos:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        self.total_videos_label = ttk.Label(stats_frame, text="0")
        self.total_videos_label.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(stats_frame, text="Total Views:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        self.total_views_label = ttk.Label(stats_frame, text="0")
        self.total_views_label.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(stats_frame, text="Total Likes:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        self.total_likes_label = ttk.Label(stats_frame, text="0")
        self.total_likes_label.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(stats_frame, text="Average Views:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        self.avg_views_label = ttk.Label(stats_frame, text="0")
        self.avg_views_label.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(stats_frame, text="Most Popular Video:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        self.popular_video_label = ttk.Label(stats_frame, text="None")
        self.popular_video_label.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Refresh button
        ttk.Button(stats_frame, text="Refresh Stats", command=self.refresh_stats).grid(row=5, column=0, padx=5, pady=10)
        
        # Refresh stats on tab open
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)
        
    def setup_search_tab(self):
        # Search frame
        search_frame = ttk.Frame(self.search_frame)
        search_frame.pack(padx=10, pady=5, fill=tk.X)
        
        ttk.Label(search_frame, text="Search:").pack(side=tk.LEFT, padx=5)
        self.search_entry = ttk.Entry(search_frame, width=40)
        self.search_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        ttk.Button(search_frame, text="Search", command=self.perform_search).pack(side=tk.LEFT, padx=5)
        
        # Results frame
        results_frame = ttk.LabelFrame(self.search_frame, text="Search Results")
        results_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        # Treeview for search results
        columns = ("type", "id", "name", "details")
        self.search_tree = ttk.Treeview(results_frame, columns=columns, show="headings")
        
        # Define headings
        self.search_tree.heading("type", text="Type")
        self.search_tree.heading("id", text="ID")
        self.search_tree.heading("name", text="Name/Title")
        self.search_tree.heading("details", text="Details")
        
        # Define columns
        self.search_tree.column("type", width=80, anchor=tk.CENTER)
        self.search_tree.column("id", width=50, anchor=tk.CENTER)
        self.search_tree.column("name", width=200, anchor=tk.W)
        self.search_tree.column("details", width=300, anchor=tk.W)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.search_tree.yview)
        self.search_tree.configure(yscrollcommand=scrollbar.set)
        
        self.search_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def on_tab_changed(self, event):
        if self.notebook.index(self.notebook.select()) == 2:  # Channel Stats tab
            self.refresh_stats()
            
    def refresh_stats(self):
        total_videos = len(self.videos)
        total_views = sum(video.get('views', 0) for video in self.videos)
        total_likes = sum(video.get('likes', 0) for video in self.videos)
        avg_views = total_views / total_videos if total_videos > 0 else 0
        
        # Find most popular video
        popular_video = None
        if self.videos:
            popular_video = max(self.videos, key=lambda x: x.get('views', 0))
        
        # Update labels
        self.total_videos_label.config(text=str(total_videos))
        self.total_views_label.config(text=str(total_views))
        self.total_likes_label.config(text=str(total_likes))
        self.avg_views_label.config(text=f"{avg_views:.2f}")
        
        if popular_video:
            self.popular_video_label.config(text=f"{popular_video['title']} ({popular_video.get('views', 0)} views)")
        else:
            self.popular_video_label.config(text="None")
            
    def perform_search(self):
        query = self.search_entry.get().lower()
        self.search_tree.delete(*self.search_tree.get_children())
        
        if not query:
            return
            
        # Search videos
        for video in self.videos:
            if query in video['title'].lower() or query in video.get('description', '').lower():
                self.search_tree.insert("", tk.END, values=(
                    "Video", 
                    video['id'], 
                    video['title'], 
                    f"{video.get('views', 0)} views, {video.get('likes', 0)} likes"
                ))
                
        # Search playlists
        for playlist in self.playlists:
            if query in playlist['name'].lower() or query in playlist.get('description', '').lower():
                self.search_tree.insert("", tk.END, values=(
                    "Playlist", 
                    playlist['id'], 
                    playlist['name'], 
                    f"{len(playlist.get('videos', []))} videos"
                ))
    
    def refresh_videos(self):
        # Clear existing items
        self.video_tree.delete(*self.video_tree.get_children())
        
        # Add videos to treeview
        for video in self.videos:
            self.video_tree.insert("", tk.END, values=(
                video['id'],
                video['title'],
                video.get('views', 0),
                video.get('likes', 0),
                video.get('upload_date', 'N/A')
            ))
            
    def refresh_playlists(self):
        # Clear existing items
        self.playlist_tree.delete(*self.playlist_tree.get_children())
        
        # Add playlists to treeview
        for playlist in self.playlists:
            self.playlist_tree.insert("", tk.END, values=(
                playlist['id'],
                playlist['name'],
                len(playlist.get('videos', [])),
                playlist.get('created_date', 'N/A')
            ))
            
    def on_video_select(self, event):
        selection = self.video_tree.selection()
        if not selection:
            return
            
        # Clear detail frame
        for widget in self.detail_frame.winfo_children():
            widget.destroy()
            
        # Get selected video
        item = self.video_tree.item(selection[0])
        video_id = item['values'][0]
        
        # Find video in list
        video = next((v for v in self.videos if v['id'] == video_id), None)
        if not video:
            return
            
        # Display video details
        ttk.Label(self.detail_frame, text=f"Title: {video['title']}").pack(anchor=tk.W, padx=5, pady=2)
        ttk.Label(self.detail_frame, text=f"Views: {video.get('views', 0)}").pack(anchor=tk.W, padx=5, pady=2)
        ttk.Label(self.detail_frame, text=f"Likes: {video.get('likes', 0)}").pack(anchor=tk.W, padx=5, pady=2)
        ttk.Label(self.detail_frame, text=f"Upload Date: {video.get('upload_date', 'N/A')}").pack(anchor=tk.W, padx=5, pady=2)
        
        description = video.get('description', 'No description')
        ttk.Label(self.detail_frame, text="Description:").pack(anchor=tk.W, padx=5, pady=2)
        desc_text = scrolledtext.ScrolledText(self.detail_frame, width=60, height=4)
        desc_text.pack(padx=5, pady=2, fill=tk.X)
        desc_text.insert(tk.END, description)
        desc_text.config(state=tk.DISABLED)
        
    def add_video(self):
        self.open_video_dialog()
        
    def edit_video(self):
        selection = self.video_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a video to edit")
            return
            
        item = self.video_tree.item(selection[0])
        video_id = item['values'][0]
        video = next((v for v in self.videos if v['id'] == video_id), None)
        
        if video:
            self.open_video_dialog(video)
        
    def delete_video(self):
        selection = self.video_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a video to delete")
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this video?"):
            item = self.video_tree.item(selection[0])
            video_id = item['values'][0]
            
            # Remove from videos
            self.videos = [v for v in self.videos if v['id'] != video_id]
            
            # Remove from playlists
            for playlist in self.playlists:
                if 'videos' in playlist and video_id in playlist['videos']:
                    playlist['videos'].remove(video_id)
            
            self.refresh_videos()
            self.save_data()
            messagebox.showinfo("Success", "Video deleted successfully")
        
    def open_video_dialog(self, video=None):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Video" if not video else "Edit Video")
        dialog.geometry("500x400")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Video form
        ttk.Label(dialog, text="Title:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        title_entry = ttk.Entry(dialog, width=40)
        title_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(dialog, text="Description:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        desc_text = scrolledtext.ScrolledText(dialog, width=40, height=5)
        desc_text.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(dialog, text="Views:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        views_entry = ttk.Entry(dialog, width=20)
        views_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(dialog, text="Likes:").grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
        likes_entry = ttk.Entry(dialog, width=20)
        likes_entry.grid(row=3, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(dialog, text="Upload Date:").grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
        date_entry = ttk.Entry(dialog, width=20)
        date_entry.grid(row=4, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Pre-fill if editing
        if video:
            title_entry.insert(0, video['title'])
            desc_text.insert(tk.END, video.get('description', ''))
            views_entry.insert(0, str(video.get('views', 0)))
            likes_entry.insert(0, str(video.get('likes', 0)))
            date_entry.insert(0, video.get('upload_date', ''))
        
        def save_video():
            # Validate inputs
            if not title_entry.get().strip():
                messagebox.showerror("Error", "Title is required")
                return
                
            try:
                views = int(views_entry.get() or 0)
                likes = int(likes_entry.get() or 0)
            except ValueError:
                messagebox.showerror("Error", "Views and Likes must be numbers")
                return
                
            # Create or update video
            if video:
                # Update existing video
                video['title'] = title_entry.get().strip()
                video['description'] = desc_text.get("1.0", tk.END).strip()
                video['views'] = views
                video['likes'] = likes
                video['upload_date'] = date_entry.get().strip()
                messagebox.showinfo("Success", "Video updated successfully")
            else:
                # Create new video
                new_id = max([v['id'] for v in self.videos], default=0) + 1
                new_video = {
                    'id': new_id,
                    'title': title_entry.get().strip(),
                    'description': desc_text.get("1.0", tk.END).strip(),
                    'views': views,
                    'likes': likes,
                    'upload_date': date_entry.get().strip()
                }
                self.videos.append(new_video)
                messagebox.showinfo("Success", "Video added successfully")
                
            self.refresh_videos()
            self.save_data()
            dialog.destroy()
            
        # Buttons
        btn_frame = ttk.Frame(dialog)
        btn_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Save", command=save_video).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
    def add_playlist(self):
        self.open_playlist_dialog()
        
    def edit_playlist(self):
        selection = self.playlist_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a playlist to edit")
            return
            
        item = self.playlist_tree.item(selection[0])
        playlist_id = item['values'][0]
        playlist = next((p for p in self.playlists if p['id'] == playlist_id), None)
        
        if playlist:
            self.open_playlist_dialog(playlist)
        
    def delete_playlist(self):
        selection = self.playlist_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a playlist to delete")
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to delete this playlist?"):
            item = self.playlist_tree.item(selection[0])
            playlist_id = item['values'][0]
            
            self.playlists = [p for p in self.playlists if p['id'] != playlist_id]
            self.refresh_playlists()
            self.save_data()
            messagebox.showinfo("Success", "Playlist deleted successfully")
            
    def view_playlist(self):
        selection = self.playlist_tree.selection()
        if not selection:
            messagebox.showwarning("Warning", "Please select a playlist to view")
            return
            
        item = self.playlist_tree.item(selection[0])
        playlist_id = item['values'][0]
        playlist = next((p for p in self.playlists if p['id'] == playlist_id), None)
        
        if not playlist:
            return
            
        dialog = tk.Toplevel(self.root)
        dialog.title(f"Playlist: {playlist['name']}")
        dialog.geometry("600x400")
        dialog.transient(self.root)
        
        # Playlist info
        info_frame = ttk.Frame(dialog)
        info_frame.pack(padx=10, pady=5, fill=tk.X)
        
        ttk.Label(info_frame, text=f"Name: {playlist['name']}").pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"Created: {playlist.get('created_date', 'N/A')}").pack(anchor=tk.W)
        ttk.Label(info_frame, text=f"Videos: {len(playlist.get('videos', []))}").pack(anchor=tk.W)
        
        # Videos in playlist
        list_frame = ttk.LabelFrame(dialog, text="Videos in Playlist")
        list_frame.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        
        columns = ("id", "title", "views")
        tree = ttk.Treeview(list_frame, columns=columns, show="headings")
        
        tree.heading("id", text="ID")
        tree.heading("title", text="Title")
        tree.heading("views", text="Views")
        
        tree.column("id", width=50, anchor=tk.CENTER)
        tree.column("title", width=300, anchor=tk.W)
        tree.column("views", width=80, anchor=tk.CENTER)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add videos to treeview
        for video_id in playlist.get('videos', []):
            video = next((v for v in self.videos if v['id'] == video_id), None)
            if video:
                tree.insert("", tk.END, values=(video['id'], video['title'], video.get('views', 0)))
                
        # Button to remove video from playlist
        def remove_video():
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("Warning", "Please select a video to remove")
                return
                
            item = tree.item(selection[0])
            video_id = item['values'][0]
            
            if video_id in playlist['videos']:
                playlist['videos'].remove(video_id)
                self.save_data()
                # Refresh the treeview
                tree.delete(selection[0])
                messagebox.showinfo("Success", "Video removed from playlist")
        
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(padx=10, pady=5, fill=tk.X)
        
        ttk.Button(btn_frame, text="Remove Video", command=remove_video).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Close", command=dialog.destroy).pack(side=tk.RIGHT, padx=5)
        
    def open_playlist_dialog(self, playlist=None):
        dialog = tk.Toplevel(self.root)
        dialog.title("Add Playlist" if not playlist else "Edit Playlist")
        dialog.geometry("500x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        # Playlist form
        ttk.Label(dialog, text="Name:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        name_entry = ttk.Entry(dialog, width=40)
        name_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)
        
        ttk.Label(dialog, text="Description:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        desc_text = scrolledtext.ScrolledText(dialog, width=40, height=5)
        desc_text.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)
        
        # Available videos
        ttk.Label(dialog, text="Available Videos:").grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
        video_frame = ttk.Frame(dialog)
        video_frame.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)
        
        video_listbox = tk.Listbox(video_frame, width=40, height=6, selectmode=tk.MULTIPLE)
        scrollbar = ttk.Scrollbar(video_frame, orient=tk.VERTICAL, command=video_listbox.yview)
        video_listbox.configure(yscrollcommand=scrollbar.set)
        
        video_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Add videos to listbox
        for video in self.videos:
            video_listbox.insert(tk.END, f"{video['id']}: {video['title']}")
        
        # Pre-fill if editing
        selected_indices = []
        if playlist:
            name_entry.insert(0, playlist['name'])
            desc_text.insert(tk.END, playlist.get('description', ''))
            
            # Select videos that are in the playlist
            for i, video in enumerate(self.videos):
                if video['id'] in playlist.get('videos', []):
                    selected_indices.append(i)
        
        # Select items in listbox
        for i in selected_indices:
            video_listbox.select_set(i)
        
        def save_playlist():
            if not name_entry.get().strip():
                messagebox.showerror("Error", "Name is required")
                return
                
            # Get selected videos
            selected_videos = []
            for i in video_listbox.curselection():
                video_id = self.videos[i]['id']
                selected_videos.append(video_id)
                
            if playlist:
                # Update existing playlist
                playlist['name'] = name_entry.get().strip()
                playlist['description'] = desc_text.get("1.0", tk.END).strip()
                playlist['videos'] = selected_videos
                messagebox.showinfo("Success", "Playlist updated successfully")
            else:
                # Create new playlist
                new_id = max([p['id'] for p in self.playlists], default=0) + 1
                new_playlist = {
                    'id': new_id,
                    'name': name_entry.get().strip(),
                    'description': desc_text.get("1.0", tk.END).strip(),
                    'videos': selected_videos,
                    'created_date': datetime.now().strftime("%Y-%m-%d")
                }
                self.playlists.append(new_playlist)
                messagebox.showinfo("Success", "Playlist added successfully")
                
            self.refresh_playlists()
            self.save_data()
            dialog.destroy()
            
        # Buttons
        btn_frame = ttk.Frame(dialog)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=10)
        
        ttk.Button(btn_frame, text="Save", command=save_playlist).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Cancel", command=dialog.destroy).pack(side=tk.LEFT, padx=5)
        
    def load_data(self):
        # Try to load data from file
        try:
            if os.path.exists("youtube_data.json"):
                with open("youtube_data.json", "r") as f:
                    data = json.load(f)
                    self.videos = data.get('videos', [])
                    self.playlists = data.get('playlists', [])
        except:
            # If loading fails, start with empty data
            self.videos = []
            self.playlists = []
            
    def save_data(self):
        # Save data to file
        data = {
            'videos': self.videos,
            'playlists': self.playlists
        }
        
        with open("youtube_data.json", "w") as f:
            json.dump(data, f, indent=2)

def main():
    root = tk.Tk()
    app = YouTubeManagerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
