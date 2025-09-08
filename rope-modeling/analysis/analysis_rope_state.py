import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import glob
from pathlib import Path


class RopeStateAnalyzer:
    def __init__(self, fps=30,n_particles=10,csv_directory="."):
        """
        Initialize the rope state analyzer.

        Args:
            csv_directory (str): Directory containing CSV files ending with
                               'simulation.csv'
        """
        self.csv_directory = csv_directory
        self.fps = fps
        self.save_dir = os.path.join(csv_directory,"result")
        os.makedirs(self.save_dir, exist_ok=True)
        self.simulation_files = self._find_simulation_files()
        self.n_particles = n_particles

    def _find_simulation_files(self):
        """Find all CSV files ending with 'simulation.csv'"""
        pattern = os.path.join(self.csv_directory, "*simulation.csv")
        files = glob.glob(pattern)
        print(f"Found {len(files)} simulation files:")
        for file in files:
            print(f"  - {os.path.basename(file)}")
        return files

    def load_simulation_data(self, filename):
        """
        Load simulation data from CSV file.

        Args:
            filename (str): Name of the CSV file

        Returns:
            tuple: (data, num_particles, num_steps)
        """
        filepath = os.path.join(self.csv_directory, filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")

        # Load CSV data
        data = pd.read_csv(filepath)

        # Extract number of particles and steps
        num_steps = len(data)
        particle_columns = [col for col in data.columns
                          if col.startswith('Particle')]
        num_particles = len(particle_columns) // 3  # X, Y, Z for each particle

        print(f"Loaded {filename}:")
        print(f"  - Steps: {num_steps}")
        print(f"  - Particles: {num_particles}")

        return data, num_particles, num_steps

    def extract_particle_positions(self, data, particle_idx):
        """
        Extract X, Y, Z positions for a specific particle.

        Args:
            data (pd.DataFrame): Simulation data
            particle_idx (int): Particle index

        Returns:
            tuple: (x_positions, y_positions, z_positions)
        """
        x_col = f'Particle{particle_idx}_X'
        y_col = f'Particle{particle_idx}_Y'
        z_col = f'Particle{particle_idx}_Z'

        x_positions = data[x_col].values
        y_positions = data[y_col].values
        z_positions = data[z_col].values

        return x_positions, y_positions, z_positions

    def plot_trajectories(self, filename, save_plot=True):
        """
        Plot X, Y, Z trajectories for initial, middle, and end particles.

        Args:
            filename (str): Name of the CSV file
            save_plot (bool): Whether to save the plot
        """
        data, num_particles, num_steps = self.load_simulation_data(filename)

        # Define particles to plot
        initial_particle = 0
        middle_particle = self.n_particles // 2
        end_particle = self.n_particles - 1

        particles_to_plot = [initial_particle, middle_particle, end_particle]
        particle_names = ['Initial', 'Middle', 'End']
        colors = ['red', 'blue', 'green']

        # Create subplots for X, Y, Z trajectories
        fig, axes = plt.subplots(3, 1, figsize=(12, 10))
        fig.suptitle(f'Particle Trajectories - {filename}', fontsize=16)

        for i, (particle_idx, name, color) in enumerate(zip(particles_to_plot, particle_names, colors)):
            x_pos, y_pos, z_pos = self.extract_particle_positions(data, particle_idx)

            # Plot X trajectory
            axes[0].plot(range(num_steps), x_pos, color=color, label=f'{name} Particle', linewidth=2)
            axes[0].set_ylabel('X Position')
            axes[0].grid(True, alpha=0.3)
            axes[0].legend()

            # Plot Y trajectory
            axes[1].plot(range(num_steps), y_pos, color=color, linewidth=2)
            axes[1].set_ylabel('Y Position')
            axes[1].grid(True, alpha=0.3)

            # Plot Z trajectory
            axes[2].plot(range(num_steps), z_pos, color=color, linewidth=2)
            axes[2].set_ylabel('Z Position')
            axes[2].set_xlabel('Simulation Step')
            axes[2].grid(True, alpha=0.3)

        plt.tight_layout()

        if save_plot:
            plot_filename = os.path.join(self.save_dir, filename.replace('.csv', '_trajectories.png'))
            plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
            print(f"Trajectory plot saved as: {plot_filename}")
            plt.clf()

    def create_3d_rope_visualization(self, filename, save_video=True):
        """
        Create 3D visualization of the rope and generate a video.

        Args:
            filename (str): Name of the CSV file
            save_video (bool): Whether to save the video
        """
        data, num_particles, num_steps = self.load_simulation_data(filename)

        # Set up the 3D figure
        fig = plt.figure(figsize=(12, 8))
        ax = fig.add_subplot(111, projection='3d')

        # Get position ranges for consistent axis limits
        all_x, all_y, all_z = [], [], []
        for i in range(self.n_particles):
            x_pos, y_pos, z_pos = self.extract_particle_positions(data, i)
            all_x.extend(x_pos)
            all_y.extend(y_pos)
            all_z.extend(z_pos)

        x_min, x_max = min(all_x), max(all_x)
        y_min, y_max = min(all_y), max(all_y)
        z_min, z_max = min(all_z), max(all_z)

        # Add some padding to the axis limits
        padding = 0.1
        x_range = x_max - x_min
        y_range = y_max - y_min
        z_range = z_max - z_min

        ax.set_xlim(x_min - padding * x_range, x_max + padding * x_range)
        ax.set_ylim(y_min - padding * y_range, y_max + padding * y_range)
        ax.set_zlim(z_min - padding * z_range, z_max + padding * z_range)

        ax.set_xlabel('X Position')
        ax.set_ylabel('Y Position')
        ax.set_zlabel('Z Position')
        ax.set_title(f'3D Rope Visualization - {filename}')

        # Initialize scatter plot for particles
        scatter = ax.scatter([], [], [], c='blue', s=50, alpha=0.8)

        # Initialize line plot for rope connections
        line, = ax.plot([], [], [], 'r-', linewidth=2, alpha=0.6)

        def animate(frame):
            # Update particle positions
            x_positions = []
            y_positions = []
            z_positions = []

            for i in range(self.n_particles):
                x_pos, y_pos, z_pos = self.extract_particle_positions(data, i)
                x_positions.append(x_pos[frame])
                y_positions.append(y_pos[frame])
                z_positions.append(z_pos[frame])

            # Update scatter plot
            scatter._offsets3d = (x_positions, y_positions, z_positions)

            # Update line plot (connect particles in sequence)
            line.set_data(x_positions, y_positions)
            line.set_3d_properties(z_positions)

            # Update title with current step
            ax.set_title(f'3D Rope Visualization - {filename} (Step {frame})')

            return scatter, line

        # Create animation
        anim = animation.FuncAnimation(
            fig, animate, frames=num_steps,
            interval=1000//self.fps, blit=False, repeat=True
        )

        if save_video:
            video_filename = os.path.join(self.save_dir, filename.replace('.csv', '_3d_visualization.mp4'))
            print(f"Creating video: {video_filename}")
            anim.save(video_filename, writer='ffmpeg', fps=self.fps, dpi=100)
            print(f"Video saved as: {video_filename}")
            plt.clf()

        return anim

    def plot_all_trajectories_combined(self, save_plot=True):
        """
        Plot trajectories from all CSV files in one combined plot.

        Args:
            save_plot (bool): Whether to save the plot
        """
        if not self.simulation_files:
            print("No simulation files found!")
            return

        # Create subplots for X, Y, Z trajectories
        fig, axes = plt.subplots(3, 1, figsize=(15, 12))
        fig.suptitle('Combined Particle Trajectories - All Simulations', fontsize=16)

        # Define colors for different simulations
        simulation_colors = ['red', 'blue', 'green', 'orange', 'purple', 'brown', 'pink', 'gray']

        for file_idx, filename in enumerate(self.simulation_files):
            try:
                data, num_particles, num_steps = self.load_simulation_data(os.path.basename(filename))

                # Define particles to plot
                initial_particle = 0
                middle_particle = num_particles // 2
                end_particle = num_particles - 1

                particles_to_plot = [initial_particle, middle_particle, end_particle]
                particle_names = ['Initial', 'Middle', 'End']

                color = simulation_colors[file_idx % len(simulation_colors)]
                sim_name = os.path.basename(filename).replace('_simulation.csv', '')

                for i, (particle_idx, name) in enumerate(zip(particles_to_plot, particle_names)):
                    x_pos, y_pos, z_pos = self.extract_particle_positions(data, particle_idx)

                    # Plot X trajectory
                    axes[0].plot(range(num_steps), x_pos, color=color,
                                label=f'{sim_name} - {name}', linewidth=2, alpha=0.8)
                    axes[0].set_ylabel('X Position')
                    axes[0].grid(True, alpha=0.3)

                    # Plot Y trajectory
                    axes[1].plot(range(num_steps), y_pos, color=color, linewidth=2, alpha=0.8)
                    axes[1].set_ylabel('Y Position')
                    axes[1].grid(True, alpha=0.3)

                    # Plot Z trajectory
                    axes[2].plot(range(num_steps), z_pos, color=color, linewidth=2, alpha=0.8)
                    axes[2].set_ylabel('Z Position')
                    axes[2].set_xlabel('Simulation Step')
                    axes[2].grid(True, alpha=0.3)

            except Exception as e:
                print(f"Error processing {filename}: {e}")
                continue

        # Add legend to first subplot
        axes[0].legend(bbox_to_anchor=(1.05, 1), loc='upper left')

        plt.tight_layout()

        if save_plot:
            plot_filename = os.path.join(self.save_dir, 'combined_trajectories.png')
            plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
            print(f"Combined trajectory plot saved as: {plot_filename}")
            plt.clf()

    def create_comprehensive_analysis(self, filename):
        """
        Create comprehensive analysis including trajectories and 3D visualization.

        Args:
            filename (str): Name of the CSV file
        """
        print(f"\n{'='*60}")
        print(f"ANALYZING: {filename}")
        print(f"{'='*60}")

        # Plot trajectories
        self.plot_trajectories(filename)

        # Create 3D visualization
        self.create_3d_rope_visualization(filename)

        # Additional analysis
        self._analyze_rope_properties(filename)

    def _analyze_rope_properties(self, filename):
        """
        Analyze rope properties like length changes, energy, etc.

        Args:
            filename (str): Name of the CSV file
        """
        data, num_particles, num_steps = self.load_simulation_data(filename)

        # Calculate rope length over time
        lengths = []
        for step in range(num_steps):
            total_length = 0
            for i in range(self.n_particles - 1):
                x1, y1, z1 = self.extract_particle_positions(data, i)
                x2, y2, z2 = self.extract_particle_positions(data, i + 1)

                segment_length = np.sqrt(
                    (x2[step] - x1[step])**2 +
                    (y2[step] - y1[step])**2 +
                    (z2[step] - z1[step])**2
                )
                total_length += segment_length
            lengths.append(total_length)

        # Plot rope length over time
        plt.figure(figsize=(10, 6))
        plt.plot(range(num_steps), lengths, 'b-', linewidth=2)
        plt.xlabel('Simulation Step')
        plt.ylabel('Rope Length')
        plt.title(f'Rope Length Over Time - {filename}')
        plt.grid(True, alpha=0.3)

        # Add statistics
        mean_length = np.mean(lengths)
        std_length = np.std(lengths)
        plt.axhline(y=mean_length, color='r', linestyle='--', alpha=0.7,
                   label=f'Mean: {mean_length:.3f}')
        plt.legend()

        plot_filename = os.path.join(self.save_dir, filename.replace('.csv', '_length_analysis.png'))
        plt.savefig(plot_filename, dpi=300, bbox_inches='tight')
        print(f"Length analysis plot saved as: {plot_filename}")
        plt.clf()

        print(f"Rope Length Statistics:")
        print(f"  - Mean length: {mean_length:.3f}")
        print(f"  - Std deviation: {std_length:.3f}")
        print(f"  - Min length: {min(lengths):.3f}")
        print(f"  - Max length: {max(lengths):.3f}")

    def analyze_all_simulations(self):
        """Analyze all simulation files found in the directory."""
        if not self.simulation_files:
            print("No simulation files found!")
            return

        print(f"\n{'='*80}")
        print(f"COMPREHENSIVE ANALYSIS OF {len(self.simulation_files)} SIMULATION(S)")
        print(f"{'='*80}")

        # First, create combined trajectory plot
        print("\nCreating combined trajectory plot...")
        self.plot_all_trajectories_combined()

        # Then analyze each simulation individually
        for filename in self.simulation_files:
            try:
                self.create_comprehensive_analysis(os.path.basename(filename))
            except Exception as e:
                print(f"Error analyzing {filename}: {e}")
                continue

def main(fps=30,n_particles=10,csv_directory="."):
    """Main function to run the analysis."""

    # Initialize analyzer
    analyzer = RopeStateAnalyzer(fps=fps, n_particles=n_particles, csv_directory=csv_directory)

    # Check if simulation files exist
    if not analyzer.simulation_files:
        print("No simulation files found! Please run the C++ simulation first.")
        print("Looking for files ending with 'simulation.csv'")
        return

    # Analyze all simulations
    analyzer.analyze_all_simulations()

    print(f"\n{'='*80}")
    print("ANALYSIS COMPLETE!")
    print("Generated files:")
    print("  - *_trajectories.png: Particle trajectory plots")
    print("  - *_3d_visualization.mp4: 3D rope animation videos")
    print("  - *_length_analysis.png: Rope length analysis")
    print(f"{'='*80}")

if __name__ == "__main__":
    _fps = 30
    n_particles = 10
    csv_directory =r"C:\Users\kawaw\cpp\rope-modeling\pbd\PBD\PBD\csv"
    main(fps=_fps,n_particles=n_particles,csv_directory=csv_directory)
