import torch
import numpy as np
import matplotlib.pyplot as plt
import sys
import os

def main():

    optimize_type = 'hyperboloid'
    phasefield = np.load('phase_and_aperture/golay_with_hyperboloid_phase_grid_5.6_um.npy')
    aperture = np.load('phase_and_aperture/golay_aperture_transmission.npy')

    f = 356000 # In um
    grid = 5.6 # In um
    wavelength_nominal = 4.500 # In um


    def asprop(e, z, λ, d):
            """
            Angular Spectrum method of propagation on unshifted complex field (unitless)
            INPUTS:
                e: [complex torch.Tensor] amplitude field; e.g.: E*exp(j*phi)
                z: distance to propagation plane; e.g.: 1e3
                λ: [float] wavelength > 0
                d: [tuple] size of meta-cell (nx>0, ny>0); size of pixels
            OUTPUT:
                stack of complex field in propagation plane(s)
            """
            # invert field phase for back-propagation
            if np.sign(z.detach().numpy()) < 0:
                e = torch.conj(e)
            # compute angular spectrum
            E = torch.fft.fft2(e)
            del e
            # extract grid parameters
            nx, ny = E.shape
            dx, dy = d
            # get k-grid (spatial frequency); real mode:propagating; complex mode: evanescent
            u = torch.fft.fftfreq(n=nx, d=dx)
            v = torch.fft.fftfreq(n=ny, d=dy)
            V, U = torch.meshgrid(v, u, indexing="ij")
            W = torch.sqrt(0j + 1/λ ** 2 - U ** 2 - V ** 2).real
            del V
            del U
            # calculate diffraction plane angular spectrum
            Ez = E * torch.exp(1j * 2 * np.pi * W * torch.abs(z))
            del E
            # retrieve diffraction-plane real-space field
            ez = torch.fft.ifft2(Ez)
            del Ez

            return ez

    wavelength = torch.tensor(float(sys.argv[1]))
    phasefield = phasefield % (2 * np.pi)       
    phasefield_def = phasefield * wavelength_nominal / (wavelength.detach().numpy())       
    del phasefield

    efield = aperture * np.exp(1j * phasefield_def)
    del phasefield_def
    del aperture

    propfield = asprop(torch.tensor(efield), torch.tensor(f), wavelength, (torch.tensor(grid), torch.tensor(grid)))

    psf_size = 200

    #Intensity
    propfield_cropped = propfield[int((len(propfield) - psf_size) / 2) : int((len(propfield) + psf_size) / 2), int((len(propfield) - psf_size) / 2) : int((len(propfield) + psf_size) / 2)]
    del propfield

    #The intensity image to be shown as the 2d PSF
    psf_cropped = np.abs(propfield_cropped) ** 2

    #Save 2d psf
    
    folder_path = os.path.join(os.path.dirname(__file__), f"grid{grid}/psf_golay/{optimize_type}")
    os.makedirs(folder_path, exist_ok=True)
    file_path = os.path.join(folder_path, f"{optimize_type}_golay_psf_{wavelength.detach().numpy():.3f}_2d.npy")
    np.save(file_path, psf_cropped.detach().numpy())

    psf_x = torch.linspace(-psf_size * grid/2, psf_size * grid/2, psf_size)
    #Show 2d psf
    plt.figure()
    plt.imshow(psf_cropped, extent=[-psf_size * grid / 2, psf_size * grid / 2, -psf_size * grid / 2, psf_size * grid / 2])
    plt.xlabel('x (μm)')
    plt.ylabel('y (μm)')
    plt.savefig(os.path.join(folder_path, f"{optimize_type}_golay_psf_{wavelength.detach().numpy():.3f}_2d.png"))


    #Show 1d psf
    plt.figure(figsize = (9, 7.2))
    middle_row_index = len(psf_cropped) // 2
    middle_row = psf_cropped[middle_row_index, :]
    plt.plot(psf_x, middle_row)
    plt.xlabel('x (μm)', fontsize=14)
    plt.ylabel('Intensity', fontsize=14)
    plt.xticks(fontsize=12)
    plt.yticks(fontsize=12)
    plt.savefig(os.path.join(folder_path, f"{optimize_type}_golay_psf_{wavelength.detach().numpy():.3f}_1d.png"))

if __name__ == "__main__":
    main()