%{?_javapackages_macros:%_javapackages_macros}

%define commit 72a20515d876081d34704bd042d2a9748b7e63a9
%define shortcommit %(c=%{commit}; echo ${c:0:7})

Summary:	An implementation of the OTR (Off The Record) protocol in Java
Name:		otr4j
Version:	0.23.0
Release:	1
License:	ASL 2.0
Group:		Development/Java
URL:		http://github.com/jitsi/otr4j
Source0:	https://github.com/jitsi/%{name}/archive/%{commit}/%{name}-%{commit}.zip
BuildArch:	noarch

BuildRequires:	maven-local
BuildRequires:	mvn(junit:junit)
BuildRequires:	mvn(org.apache.commons:commons-lang3)
BuildRequires:	mvn(org.apache.maven.plugins:maven-failsafe-plugin)
BuildRequires:	mvn(org.apache.maven.plugins:maven-gpg-plugin)
BuildRequires:	mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires:	mvn(org.bouncycastle:bcprov-jdk15on)
BuildRequires:	mvn(org.mockito:mockito-all)

%description
otr4j is an implementation of the OTR (Off The Record) protocol in Java.

Off-the-Record Messaging, is a cryptographic protocol that uses a combination
of the Advanced Encryption Standard (AES), the Diffie-Hellman key exchange,
and the SHA hash functions. In addition to authentication and encryption, OTR
provides perfect forward secrecy and malleable encryption.

The OTR protocol was designed by Ian Goldberg and the OTR Development Team.

%files -f .mfiles
%doc README.markdown
%doc THANKS.markdown
%doc TODO.txt
%doc LICENSE
%doc docs

#----------------------------------------------------------------------------

%package javadoc
Summary:	Javadoc for %{name}
Requires:	jpackage-utils

%description javadoc
API documentation for %{name}.

%files javadoc -f .mfiles-javadoc

#----------------------------------------------------------------------------

%prep
%setup -q -n %{name}-%{commit}
# Delete all prebuild JARs and classes
find . -name "*.jar" -delete
find . -name "*.class" -delete

# Remove un-packaged plugin
%pom_remove_plugin :nexus-staging-maven-plugin

# Bundle
%pom_xpath_replace "pom:project/pom:packaging" "<packaging>bundle</packaging>" .

# Add an OSGi compilant MANIFEST.MF
%pom_add_plugin org.apache.felix:maven-bundle-plugin . "
<extensions>true</extensions>
<configuration>
	<supportedProjectTypes>
		<supportedProjectType>bundle</supportedProjectType>
		<supportedProjectType>jar</supportedProjectType>
	</supportedProjectTypes>
	<instructions>
		<Bundle-Name>\${project.artifactId}</Bundle-Name>
		<Bundle-Version>\${project.version}</Bundle-Version>
	</instructions>
</configuration>
<executions>
	<execution>
		<id>bundle-manifest</id>
		<phase>process-classes</phase>
		<goals>
			<goal>manifest</goal>
		</goals>
	</execution>
</executions>"

# Add the META-INF/INDEX.LIST (fix jar-not-indexed warning) and
# the META-INF/MANIFEST.MF to the jar archive
%pom_add_plugin :maven-jar-plugin . "
<executions>
	<execution>
		<phase>package</phase>
		<configuration>
			<archive>
				<manifestFile>\${project.build.outputDirectory}/META-INF/MANIFEST.MF</manifestFile>
				<manifest>
					<addDefaultImplementationEntries>true</addDefaultImplementationEntries>
					<addDefaultSpecificationEntries>true</addDefaultSpecificationEntries>
				</manifest>
				<index>true</index>
			</archive>
		</configuration>
		<goals>
			<goal>jar</goal>
		</goals>
	</execution>
</executions>"

# Add alias
%mvn_file org.jitsi:org.%{name} org.jitsi:%{name}

# Fix jar name
%mvn_file :%{name} %{name}-%{version} %{name}

%build
%mvn_build

%install
%mvn_install

