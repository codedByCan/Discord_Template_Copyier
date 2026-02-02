import discord
import asyncio
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox

app_title = "Discord Template Copier"
geometry = "600x550"

class ServerClonerApp:
    def __init__(self, root):
        self.root = root
        self.root.title(app_title)
        self.root.geometry(geometry)
        self.root.resizable(False, False)

        self.client = None
        self.loop = asyncio.new_event_loop()
        self.bot_thread = None
        self.is_connected = False

        frame_top = ttk.LabelFrame(root, text="Authentication")
        frame_top.pack(pady=10, padx=10, fill="x")

        ttk.Label(frame_top, text="User Token:").pack(side="left", padx=5)
        self.token_entry = ttk.Entry(frame_top, show="*", width=50)
        self.token_entry.pack(side="left", padx=5)
        
        self.btn_connect = ttk.Button(frame_top, text="Login", command=self.start_bot_thread)
        self.btn_connect.pack(side="left", padx=5)

        frame_select = ttk.LabelFrame(root, text="Configuration")
        frame_select.pack(pady=10, padx=10, fill="x")

        ttk.Label(frame_select, text="Source Server (Copy From):").pack(anchor="w", padx=5, pady=2)
        self.combo_source = ttk.Combobox(frame_select, state="readonly", width=70)
        self.combo_source.pack(padx=5, pady=5)

        ttk.Label(frame_select, text="Target Server (Paste To - WILL BE WIPED):").pack(anchor="w", padx=5, pady=2)
        self.combo_target = ttk.Combobox(frame_select, state="readonly", width=70)
        self.combo_target.pack(padx=5, pady=5)

        self.btn_start = ttk.Button(root, text="START CLONING", command=self.start_cloning, state="disabled")
        self.btn_start.pack(pady=5, ipadx=10, ipady=5)

        frame_log = ttk.LabelFrame(root, text="Logs")
        frame_log.pack(pady=10, padx=10, fill="both", expand=True)

        self.log_area = scrolledtext.ScrolledText(frame_log, height=10, state='disabled', font=("Consolas", 9))
        self.log_area.pack(fill="both", expand=True, padx=5, pady=5)

    def log(self, message):
        self.log_area.config(state='normal')
        self.log_area.insert(tk.END, f"> {message}\n")
        self.log_area.see(tk.END)
        self.log_area.config(state='disabled')

    def start_bot_thread(self):
        token = self.token_entry.get()
        if not token:
            messagebox.showerror("Error", "Please enter a valid token!")
            return

        self.btn_connect.config(state="disabled")
        self.log("Initializing client...")
        
        self.bot_thread = threading.Thread(target=self.run_bot, args=(token,), daemon=True)
        self.bot_thread.start()

    def run_bot(self, token):
        asyncio.set_event_loop(self.loop)
        self.client = discord.Client()

        @self.client.event
        async def on_ready():
            self.root.after(0, self.on_bot_ready)

        try:
            self.client.run(token, bot=False)
        except Exception as e:
            self.root.after(0, lambda: self.log(f"LOGIN ERROR: {e}"))
            self.root.after(0, lambda: self.btn_connect.config(state="normal"))

    def on_bot_ready(self):
        self.is_connected = True
        self.log(f"Logged in as: {self.client.user}")
        
        guilds = []
        for guild in self.client.guilds:
            guilds.append(f"{guild.name} ({guild.id})")
        
        self.combo_source['values'] = guilds
        self.combo_target['values'] = guilds
        self.btn_start.config(state="normal")
        self.log(f"Loaded {len(guilds)} guilds.")

    def get_id_from_selection(self, selection):
        try:
            return int(selection.split('(')[-1].replace(')', ''))
        except:
            return None

    def start_cloning(self):
        source_selection = self.combo_source.get()
        target_selection = self.combo_target.get()

        if not source_selection or not target_selection:
            messagebox.showwarning("Warning", "Please select both Source and Target servers.")
            return

        source_id = self.get_id_from_selection(source_selection)
        target_id = self.get_id_from_selection(target_selection)

        if source_id == target_id:
            messagebox.showerror("Error", "Source and Target cannot be the same!")
            return
        
        confirm = messagebox.askyesno("Confirm Wipe", f"WARNING!\n\nALL DATA in '{target_selection}' will be DELETED.\nAre you sure?")
        
        if confirm:
            self.btn_start.config(state="disabled")
            asyncio.run_coroutine_threadsafe(self.clone_process(source_id, target_id), self.loop)

    async def clone_process(self, source_id, target_id):
        source_guild = self.client.get_guild(source_id)
        target_guild = self.client.get_guild(target_id)

        self.root.after(0, lambda: self.log("--- Cloning Process Started ---"))

        self.root.after(0, lambda: self.log("Cleaning: Deleting channels..."))
        for channel in target_guild.channels:
            try:
                await channel.delete()
                await asyncio.sleep(0.5)
            except:
                pass
        
        self.root.after(0, lambda: self.log("Cleaning: Deleting roles..."))
        for role in target_guild.roles:
            if role.name != "@everyone":
                try:
                    await role.delete()
                    await asyncio.sleep(0.5)
                except:
                    pass

        try:
            icon_content = await source_guild.icon_url.read()
            await target_guild.edit(name=source_guild.name, icon=icon_content)
            self.root.after(0, lambda: self.log("Server name and icon updated."))
        except:
             self.root.after(0, lambda: self.log("Could not update icon."))

        self.root.after(0, lambda: self.log("Cloning: Creating roles..."))
        roles_map = {}
        
        for role in reversed(source_guild.roles):
            if role.name != "@everyone":
                try:
                    new_role = await target_guild.create_role(
                        name=role.name,
                        permissions=role.permissions,
                        color=role.color,
                        hoist=role.hoist,
                        mentionable=role.mentionable
                    )
                    roles_map[role] = new_role
                    self.root.after(0, lambda: self.log(f"Role created: {role.name}"))
                    await asyncio.sleep(1) 
                except Exception as e:
                    self.root.after(0, lambda: self.log(f"Error (Role): {e}"))

        self.root.after(0, lambda: self.log("Cloning: Creating structure..."))
        
        for cat in source_guild.categories:
            try:
                overwrites = {}
                for role, overwrite in cat.overwrites.items():
                    if isinstance(role, discord.Role) and role in roles_map:
                        overwrites[roles_map[role]] = overwrite
                    elif role.name == "@everyone":
                         overwrites[target_guild.default_role] = overwrite

                new_cat = await target_guild.create_category(name=cat.name, overwrites=overwrites)
                
                for channel in cat.channels:
                    c_overwrites = {}
                    for role, overwrite in channel.overwrites.items():
                        if isinstance(role, discord.Role) and role in roles_map:
                            c_overwrites[roles_map[role]] = overwrite
                        elif role.name == "@everyone":
                            c_overwrites[target_guild.default_role] = overwrite

                    if isinstance(channel, discord.TextChannel):
                        await new_cat.create_text_channel(name=channel.name, topic=channel.topic, overwrites=c_overwrites, slowmode_delay=channel.slowmode_delay)
                    elif isinstance(channel, discord.VoiceChannel):
                        await new_cat.create_voice_channel(name=channel.name, user_limit=channel.user_limit, bitrate=channel.bitrate, overwrites=c_overwrites)
                    
                    self.root.after(0, lambda: self.log(f"Channel created: {channel.name}"))
                    await asyncio.sleep(1.5)

            except Exception as e:
                self.root.after(0, lambda: self.log(f"Error (Structure): {e}"))

        for channel in source_guild.text_channels:
            if channel.category is None:
                try:
                    await target_guild.create_text_channel(name=channel.name)
                except: pass
        
        self.root.after(0, lambda: self.log("--- SUCCESS ---"))
        messagebox.showinfo("Success", "Server cloned successfully!")
        self.root.after(0, lambda: self.btn_start.config(state="normal"))

if __name__ == "__main__":
    root = tk.Tk()
    app = ServerClonerApp(root)
    root.mainloop()
