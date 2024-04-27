import instaloader
import tkinter as tk
from tkinter import messagebox, filedialog
import customtkinter as ctk
import os


class InstagramDownloader(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Instagram Downloader")
        self.geometry("400x450")

        # Entrée du nom d'utilisateur Instagram
        self.username_entry = ctk.CTkEntry(self, placeholder_text="Nom d'utilisateur Instagram")
        self.username_entry.pack(pady=10)

        # Case à cocher pour télécharger la photo de profil
        self.profile_pic_var = tk.BooleanVar()
        self.profile_pic_checkbox = ctk.CTkCheckBox(self, text="Télécharger la photo de profil", variable=self.profile_pic_var)
        self.profile_pic_checkbox.pack(pady=10)

        # Case à cocher pour télécharger les publications (avec sous-options)
        self.posts_var = tk.BooleanVar()
        self.posts_checkbox = ctk.CTkCheckBox(self, text="Télécharger les publications", variable=self.posts_var)
        self.posts_checkbox.pack(pady=10)

        # Sous-options pour les publications
        self.photos_var = tk.BooleanVar()
        self.photos_checkbox = ctk.CTkCheckBox(self, text="Photos", variable=self.photos_var)
        self.photos_checkbox.pack(pady=10)

        self.videos_var = tk.BooleanVar()
        self.videos_checkbox = ctk.CTkCheckBox(self, text="Vidéos", variable=self.videos_var)
        self.videos_checkbox.pack(pady=10)

        # Case à cocher pour télécharger les stories
        self.stories_var = tk.BooleanVar()
        self.stories_checkbox = ctk.CTkCheckBox(self, text="Télécharger les stories", variable=self.stories_var)
        self.stories_checkbox.pack(pady=10)

        # Case à cocher pour les stories à la une (highlights)
        self.highlights_var = tk.BooleanVar()
        self.highlights_checkbox = ctk.CTkCheckBox(self, text="Télécharger les stories à la une", variable=self.highlights_var)
        self.highlights_checkbox.pack(pady=10)

        # Case à cocher pour les vidéos IGTV
        self.igtv_var = tk.BooleanVar()
        self.igtv_checkbox = ctk.CTkCheckBox(self, text="Télécharger les vidéos IGTV", variable=self.igtv_var)
        self.igtv_checkbox.pack(pady=10)

        # Case à cocher pour les reels
        self.reels_var = tk.BooleanVar()
        self.reels_checkbox = ctk.CTkCheckBox(self, text="Télécharger les reels", variable=self.reels_var)
        self.reels_checkbox.pack(pady=10)

        # Case à cocher pour les métadonnées
        self.metadata_var = tk.BooleanVar()
        self.metadata_checkbox = ctk.CTkCheckBox(self, text="Télécharger les métadonnées", variable=self.metadata_var)
        self.metadata_checkbox.pack(pady=10)

        # Bouton pour lancer le téléchargement
        self.download_button = ctk.CTkButton(self, text="Télécharger", command=self.download)
        self.download_button.pack(pady=10)

    def download(self):
        username = self.username_entry.get()

        # Choisir un répertoire de téléchargement
        download_path = filedialog.askdirectory(title="Sélectionnez un répertoire de téléchargement")

        if not download_path:
            messagebox.showerror("Erreur", "Aucun répertoire sélectionné. Veuillez en choisir un.")
            return

        try:
            # Instaloader avec le modèle de répertoire
            L = instaloader.Instaloader(dirname_pattern=os.path.join(download_path, "{target}"))

            # Obtenir le profil Instagram
            profile = instaloader.Profile.from_username(L.context, username)

            # Télécharger la photo de profil
            if self.profile_pic_var.get():
                L.download_profile(profile, profile_pic_only=True)

            # Télécharger les publications
            if self.posts_var.get():
                for post in profile.get_posts():
                    if self.photos_var.get() and post.is_video is False:
                        L.download_post(post, target="photos")
                    elif self.videos_var.get() and post.is_video is True:
                        L.download_post(post, target="vidéos")

            # Télécharger les stories
            if self.stories_var.get():
                for story in profile.get_stories():
                    L.download_storyitem(story, target="stories")

            # Télécharger les stories à la une
            if self.highlights_var.get():
                for highlight in profile.get_highlights():
                    L.download_storyitem(highlight, target="highlights")

            # Télécharger les vidéos IGTV
            if self.igtv_var.get():
                for igtv in profile.get_igtv_videos():
                    L.download_post(igtv, target="igtv")

            # Télécharger les reels
            if self.reels_var.get():
                for reel in profile.get_reels():
                    L.download_post(reel, target="reels")

            # Télécharger les métadonnées
            if self.metadata_var.get():
                L.download_metadata(profile, target="metadata")

            messagebox.showinfo("Succès", "Téléchargement réussi.")

        except instaloader.exceptions.ProfileNotExistsException:
            messagebox.showerror("Erreur", "Le profil Instagram spécifié n'existe pas.")
        except instaloader.exceptions.ConnectionException:
            messagebox.showerror("Erreur", "Erreur de connexion lors du téléchargement.")
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")


if __name__ == "__main__":
    app = InstagramDownloader()
    app.mainloop()
