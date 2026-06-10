{
  description = "MediaViewer MCP - FastMCP server";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";

    pyproject-nix = {
      url = "github:pyproject-nix/pyproject.nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    uv2nix = {
      url = "github:pyproject-nix/uv2nix";
      inputs.pyproject-nix.follows = "pyproject-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };

    pyproject-build-systems = {
      url = "github:pyproject-nix/build-system-pkgs";
      inputs.nixpkgs.follows = "nixpkgs";
      inputs.pyproject-nix.follows = "pyproject-nix";
    };
  };

  outputs =
    {
      self,
      nixpkgs,
      flake-utils,
      uv2nix,
      pyproject-nix,
      pyproject-build-systems,
      ...
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs { inherit system; };

        # Use Python 3.14 to match the project's requires-python
        python = pkgs.python314;

        # 1. Load project workspace (parses pyproject.toml + uv.lock)
        workspace = uv2nix.lib.workspace.loadWorkspace {
          workspaceRoot = ./.;
        };

        # 2. Generate Nix overlay from uv.lock
        overlay = workspace.mkPyprojectOverlay {
          sourcePreference = "wheel"; # Prefer wheels for faster builds
        };

        # 3. Construct the final Python package set
        pythonSet =
          (pkgs.callPackage pyproject-nix.build.packages { inherit python; })
          .overrideScope (
            nixpkgs.lib.composeManyExtensions [
              pyproject-build-systems.overlays.default
              overlay
            ]
          );

        # 4. Create the Python virtual environment with all dependencies
        appEnv = pythonSet.mkVirtualEnv "mv-mcp-env" workspace.deps.default;
      in
      {
        # Dev shell with the full environment + uv for dependency management
        devShells.default = pkgs.mkShell {
          packages = [
            appEnv
            pkgs.uv
          ];
        };

        # Nix package wrapping main.py with its runtime environment
        packages.default = pkgs.stdenv.mkDerivation {
          name = "mv-mcp";
          src = ./.;

          nativeBuildInputs = [ pkgs.makeWrapper ];
          buildInputs = [ appEnv ];

          installPhase = ''
            mkdir -p $out/bin
            cp main.py $out/bin/mv-mcp-script
            chmod +x $out/bin/mv-mcp-script
            makeWrapper ${appEnv}/bin/python $out/bin/mv-mcp \
              --add-flags "$out/bin/mv-mcp-script"
          '';

          meta = {
            description = "MediaViewer MCP server";
            mainProgram = "mv-mcp";
          };
        };

        # `nix run` starts the MCP HTTP server on port 8089
        apps.default = {
          type = "app";
          program = "${self.packages.${system}.default}/bin/mv-mcp";
        };

        # Docker image wrapping the MCP server
        # Build: nix build .#docker
        # Load:  docker load < result
        # Run:   docker run -e MV_MCP_API_KEY=... -e MV_HOST=... -p 8089:8089 mv-mcp:latest
        packages.docker = pkgs.dockerTools.buildLayeredImage {
          name = "kyokley/mv-mcp";
          tag = "latest";
          contents = [ self.packages.${system}.default ];
          config = {
            Cmd = [ "${self.packages.${system}.default}/bin/mv-mcp" ];
            ExposedPorts = { "8089/tcp" = { }; };
            Env = [
              "MV_MCP_API_KEY="
              "MV_HOST="
            ];
          };
        };
      }
    );
}
