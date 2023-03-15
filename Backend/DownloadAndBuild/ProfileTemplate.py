from Backend.DownloadAndBuild.Config import *

class ProfileTemplate:

    def Get(profile: Profile) -> str:
        return \
        f"[settings]\n" \
        f"arch={profile.arch}\n" \
        f"build_type={profile.build_type}\n" \
        f"compiler={profile.compiler}\n" \
        f"compiler.cppstd={profile.compiler_cppstd}\n" \
        f"compiler.runtime={profile.compiler_runtime}\n" \
        f"compiler.runtime_type={profile.compiler_runtime_type}\n" \
        f"compiler.version={profile.compiler_version}\n" \
        f"os={profile.os}\n"